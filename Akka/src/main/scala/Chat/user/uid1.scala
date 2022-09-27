package Chat.user

import Chat.common._
import Chat.user.User.{selfActorRef, userInformation}
import akka.actor._
import akka.pattern.ask
import akka.util.Timeout
import com.typesafe.config.ConfigFactory

import scala.concurrent.Await
import scala.concurrent.duration.DurationInt
import scala.io.StdIn
import scala.language.postfixOps
import scala.util.control.Breaks.{break, breakable}

class User(serverHost: String, serverPort: Int, nameServerActorSystem: String) extends Actor {
  implicit val timeout: Timeout = Timeout(5 seconds) //阻塞等待最多5秒
  var serverActorRef: ActorSelection = _ //用于存放远程服务器的ActorRef

  override def preStart: Unit = {
    serverActorRef = context.actorSelection(
      s"akka://Server@$serverHost:$serverPort/user/" + nameServerActorSystem) //获取远程服务器的ActorRef
  }

  override def receive: Receive = {
    case "start" => //用于初始化
      serverActorRef ! RegisterUser("user", User.selfActorRef) //用户上线第一时间把自身名称和ActorRef上传服务器
    case reply: RegisteredUser => //接收服务器的答复，判断是否注册成功，如果注册失败则退出程序
      if (reply.reply) println("成功注册，您已上线！")
      else {
        println("用户注册失败（可能是用户名已存在）")
        sys.exit() //退出程序
      }
    case message: MessageProtocol => //接收发来的聊天消息
      println(message.user + "发来消息: " + message.message)
    case userMap: UserList => User.userInformation = userMap.userInformation //接收并更新用户信息表
    case "ls" =>
      val future = serverActorRef ? UserList //向服务器发送请求，获取用户信息表，“？”表示阻塞等待
      val result = Await.result(future, timeout.duration).asInstanceOf[UserList] //result接收返回值
      userInformation = result.userInformation //更新用户信息表
      //下面输出用户信息表
      println("当前在线用户：\n用户名\tActorRef")
      if (userInformation == null) println("userInformation = null")
      else for ((k, v) <- User.userInformation) println(k + "\t" + v)
    case "exit" =>
      println("接收到exit指令，退出系统")
      serverActorRef ! Offline("user") //下线前向服务器发送消息，删除本用户信息
      context.stop(self) //这条语句和下面的语句用来退出akka
      context.system.terminate()
  }
}

object User {
  var selfActorRef: ActorRef = _ //用于存放自己的ActorRef
  var userInformation: scala.collection.mutable.HashMap[String, ActorRef] = _ //用户名和对应的ActorRef的映射表

  def main(args: Array[String]): Unit = {
    //配置本用户ip和端口和远程服务器的ip和端口，端口号为0表示随机分配可用端口号
    val (nameServerActorSystem, serverHost, serverPort, nameUserActor, userHost, userPort) =
      (args(0), args(1), args(2).toInt, args(3), args(4), 0)
    //用于配置本用户的ip和端口，”akka.actor.allow-java-serialization = "on"“表示使用java来序列化，远程发送消息需要经过序列化
    val config = ConfigFactory.parseString(
      s"""
         |akka.actor.provider = "akka.remote.RemoteActorRefProvider"
         |akka.actor.allow-java-serialization = "on"
         |akka.remote.artery.enable = "on"
         |akka.remote.artery.canonical.hostname = $userHost
         |akka.remote.artery.canonical.port = $userPort
         |""".stripMargin)
    val userActorSystem = ActorSystem("user", config) //实例化ActorSystem
    val userActorRef: ActorRef = userActorSystem.actorOf(
      Props(new User(serverHost, serverPort, nameServerActorSystem)), nameUserActor)
    selfActorRef = userActorRef
    userActorRef ! "start"
    println("ip = " + AddressExtension.hostOf(userActorSystem))
    println("端口 = " + AddressExtension.portOf(userActorSystem))
    breakable(
      while (true) {
        println("-" * 100)
        println("ls->查看并刷新用户表")
        val order = StdIn.readLine() //接收输入
        order match { //根据输入的字符串判断指令做对应操作
          case "ls" => //获取，刷新，展示用户信息表
            selfActorRef ! "ls"
          case "exit" => //关机下线
            selfActorRef ! "exit"
            break()
          case user: String => //给用户发送消息
            if (userInformation.contains(user)) {
              print("发送消息@" + user + ": ")
              val mes = StdIn.readLine()
              userInformation(user) ! MessageProtocol(nameUserActor, mes)
            } else println("用户不存在或者您的输入有误，请重新输入！")
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
