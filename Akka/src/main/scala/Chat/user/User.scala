package Chat.user

import Chat.common._
import akka.actor._
import akka.pattern.ask
import akka.util.Timeout
import com.typesafe.config.ConfigFactory

import scala.concurrent.Await
import scala.concurrent.duration.DurationInt
import scala.io.StdIn
import scala.language.postfixOps
import scala.util.control.Breaks.{break, breakable}

class User(nameServerActorSystem: String, serverHost: String, serverPort: Int, nameUserActor: String) extends Actor {
  implicit val timeout: Timeout = Timeout(5 seconds) //阻塞等待最多5秒
  var serverActorRef: ActorSelection = _ //用于存放远程服务器的ActorRef
  var lastCheckConnect: Long = System.currentTimeMillis() //System.currentTimeMillis()返回当前时间

  override def preStart: Unit = {
    serverActorRef = context.actorSelection(
      s"akka://Server@$serverHost:$serverPort/user/" + nameServerActorSystem) //获取远程服务器的ActorRef
  }

  override def receive: Receive = {
    case "start" => //用于初始化
      serverActorRef ! RegisterUser(nameUserActor, self) //用户上线第一时间把自身名称和ActorRef上传服务器
      import context.dispatcher
      context.system.scheduler.scheduleWithFixedDelay(0 millis, 9000 millis, self, CheckConnect)
    case RegisteredUser(reply) => //接收服务器的答复，判断是否注册成功，如果注册失败则退出程序
      reply match {
        case reply: Boolean =>
          if (!reply) { //如果返回的是false，提示注册失败并退出程序
            println("用户注册失败（可能是用户名已存在）")
            sys.exit() //退出程序
          }
        case reply: scala.collection.mutable.HashMap[String, UserInfo] =>
          println("成功注册，您已上线！")
          User.userInformation = reply //成功注册后立即接收并更新用户信息表
          import context.dispatcher
          //第一个参数0毫秒表示不延迟，立即执行定时器；第二个参数表示每隔3秒执行一次，第三个表示发给自己，第四个表示发送的内容
          context.system.scheduler.scheduleWithFixedDelay(0 millis, 3000 millis, self, SendHeartBeat)
      }
    case SendHeartBeat => serverActorRef ! HeartBeat(nameUserActor) //向服务器发送心跳消息
    case MessageProtocol(user, message) => //接收发来的聊天消息
      println("*"*100)
      println(user + "发来消息: " + message)
      println("*"*100)
    case UserList(userInformation) =>
      User.userInformation = userInformation //定时接收并更新用户信息表
      lastCheckConnect = System.currentTimeMillis() //收到服务器下发的用户信息表时，顺便更新最近一次与服务器连接的时间
    case CheckConnect =>
      val mistiming = System.currentTimeMillis() - lastCheckConnect
      //用现在的时间减去最近一次与服务器连接的时间相减，如果超过9秒则打印输出告诉用户当前与服务器失去连接
      if (mistiming > 9000) println("警告：服务器失去连接，连接已超时" + mistiming)
    case "ls" => //获取，刷新，展示用户信息表
      val future = serverActorRef ? UserList //向服务器发送请求，获取用户信息表，“？”表示阻塞等待
      val result = Await.result(future, timeout.duration).asInstanceOf[UserList] //result接收返回值
      User.userInformation = result.userInformation //更新用户信息表
      //下面输出用户信息表
      println("当前在线用户：\n用户名\tActorRef")
      if (User.userInformation == null) println("userInformation = null")
      else for ((k, v) <- User.userInformation) println(k + "\t" + v.userActorRef)
    case "exit" => //关机下线
      println("接收到exit指令，退出系统")
      serverActorRef ! Offline(nameUserActor) //下线前向服务器发送消息，删除本用户信息
      context.stop(self) //这条语句和下面的语句用来退出akka
      context.system.terminate()
  }
}

object User {
  var userInformation: scala.collection.mutable.HashMap[String, UserInfo] = _ //用户名和对应的ActorRef的映射表

  def main(args: Array[String]): Unit = {
    //配置本用户ip和端口和远程服务器的ip和端口，端口号为0表示随机分配可用端口号
    val (nameServerActorSystem, serverHost, serverPort, nameUserActor, userHost, userPort) =
      (args(0), args(1), args(2).toInt, args(3), args(4), 0)
    //用于配置本用户的ip和端口，”akka.actor.allow-java-serialization = "on"“表示使用java来序列化，远程发送消息需要经过序列化
    //注意：akka.actor.warn-about-java-serializer-usage = "off"这里忽略了java序列化的警告，使用java序列化性能差，不安全
    val config = ConfigFactory.parseString(
      s"""
         |akka.actor.provider = "akka.remote.RemoteActorRefProvider"
         |akka.actor.allow-java-serialization = "on"
         |akka.actor.warn-about-java-serializer-usage = "off"
         |akka.remote.artery.enable = "on"
         |akka.remote.artery.canonical.hostname = $userHost
         |akka.remote.artery.canonical.port = $userPort
         |""".stripMargin)
    val userActorSystem = ActorSystem("user", config) //实例化ActorSystem
    val userActorRef: ActorRef = userActorSystem.actorOf(
      Props(new User(nameServerActorSystem, serverHost, serverPort, nameUserActor)), nameUserActor)
    userActorRef ! "start"
    breakable(
      while (true) {
        println("-" * 100)
        println("ls->查看并刷新用户表\n”@+用户名“向用户发送消息（如@uid1）")
        println("主机名 = " + nameUserActor + "\t" +
          "ip = " + AddressExtension.hostOf(userActorSystem) + "\t" +
          "端口 = " + AddressExtension.portOf(userActorSystem))
        val order = StdIn.readLine() //接收输入
        order match { //根据输入的字符串判断指令做对应操作
          case "ls" => userActorRef ! "ls" //获取，刷新，展示用户信息表
          case "exit" => //关机下线
            userActorRef ! "exit"
            break
          case user: String => //符合”@+用户名“的格式时，判断用户存在后发送消息
            if ("".equals(user)) println() //处理掉输入的空字符串
            else if (userInformation == null) println("userInformation = null，请尝试更新用户信息表（尝试“ls”命令）")
            else if ("@".equals(user.head.toString)) {
              if (userInformation.contains(user.tail)) {
                print("发送消息@" + user.tail + ": ")
                val mes = StdIn.readLine() //接收输入
                //直接用目标用户的ActorRef发送消息
                userInformation(user.tail).userActorRef ! MessageProtocol(nameUserActor, mes)
              } else println("用户不存在，请重新输入（输入“ls”查看并刷新用户表）")
            } else println("没有匹配到命令，请重新输入！")
          case _ => println("没有匹配结果")
        }
      }
    )
  }
}

//class AddressExtension和object AddressExtension一起，调用hostOf返回ip，调用portOf返回端口
class AddressExtension(system: ExtendedActorSystem) extends Extension {
  val address: Address = system.provider.getDefaultAddress
}

//class AddressExtension和object AddressExtension一起，调用hostOf返回ip，调用portOf返回端口
object AddressExtension extends ExtensionId[AddressExtension] {
  def createExtension(system: ExtendedActorSystem): AddressExtension = new AddressExtension(system)

  def hostOf(system: ActorSystem): String = AddressExtension(system).address.host.getOrElse("")

  def portOf(system: ActorSystem): Int = AddressExtension(system).address.port.getOrElse(0)
}
