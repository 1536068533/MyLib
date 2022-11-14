package Chat.server

import Chat.common._
import akka.actor._
import com.typesafe.config.ConfigFactory

import scala.concurrent.duration.DurationInt
import scala.io.StdIn
import scala.language.postfixOps
import scala.util.control.Breaks.{break, breakable}

class TextTalkServer extends Actor {
  override def receive: Receive = {
    case "start" =>
      println("start 聊天服务器开始工作了") //可以用于初始化，做一些准备工作
      self ! StartTimeOutUser //开始心跳超时检测
      import context.dispatcher
      /*
      第一个参数0毫秒表示不延迟，立即执行定时器；第二个参数表示每隔3秒执行一次，第三个表示发给自己，第四个表示发送的内容
      对自己发送心跳，避免超时自动删除服务器在userInformation表中的记录
       */
      context.system.scheduler.scheduleWithFixedDelay(
        0 millis, 3000 millis, self, HeartBeat("server"))
      //定时每5秒对所有用户下发一次用户信息表
      context.system.scheduler.scheduleWithFixedDelay(0 millis, 5000 millis, self, SendHeartBeat)
    case _: UserList => //因为对所有用户下发用户信息表时，也包括服务器自己，所以这里接一下，不做任何处理
    case RegisterUser(userName, userActorRef) =>
      //用户名已存在，向用户答复注册失败，否则，加入用户信息表并向用户答复注册成功
      if (TextTalkServer.userInformation.contains(userName)) sender() ! RegisteredUser(false)
      else {
        val userInfo = UserInfo(userName, userActorRef) //每个用户注册都会创建一个UserInfo实例
        TextTalkServer.userInformation(userName) = userInfo //存到用户信息表中
        sender() ! RegisteredUser(TextTalkServer.userInformation) //注册成功则发送用户表信息表
      }
    case UserList => sender() ! UserList(TextTalkServer.userInformation) //如果有人查询用户列表，则返回用户列表
    //收到用户上传的心跳消息，更新用户信息表中对应用户的心跳时间
    case HeartBeat(userName) => TextTalkServer.userInformation(userName).lastHeartBeat = System.currentTimeMillis()
    case SendHeartBeat =>
      if (TextTalkServer.userInformation != null) { //避免空表
        for (userInfo <- TextTalkServer.userInformation.values) { //对所有用户下发一次用户信息表
          userInfo.userActorRef ! UserList(TextTalkServer.userInformation)
        }
      }
    case StartTimeOutUser =>
      import context.dispatcher
      //每9秒检查一次超时用户
      context.system.scheduler.scheduleWithFixedDelay(0 millis, 9000 millis, self, RemoveTimeOutUser)
    case RemoveTimeOutUser =>
      /*
      首先筛选userInformation表中的value，用现在的时间减去表中value的那个类的最近一次心跳时间记录，
      把所有大于6000毫秒的都筛选出来，最后在userInformation表中删除这些被筛选出来了的用户的信息
       */
      TextTalkServer.userInformation.values.filter(
        UserInfo => System.currentTimeMillis() - UserInfo.lastHeartBeat > 6000)
        .foreach(userInfo => TextTalkServer.userInformation.remove(userInfo.userName))
    case MessageProtocol(user, message) =>
      println("*" * 100)
      println(user + "发来消息: " + message)
      println("*" * 100)
    case Offline(user) => TextTalkServer.userInformation -= user
    case "shutdown" =>
      println("接收到shutdown指令，退出系统")
      context.stop(self) //这条语句和下面的语句用来退出akka
      context.system.terminate()
  }
}

object TextTalkServer {
  val userInformation = new scala.collection.mutable.HashMap[String, UserInfo] //用户名和对应的ActorRef的映射表

  def main(args: Array[String]): Unit = {
    //检验参数
    if(args.length != 1){
      println("[error] 运行需要ip地址参数，例如：java -jar xxx.jar 127.0.0.1")
      sys.exit() //退出程序
    }
    val (host, port) = (args(0), 0) //指定本服务器的ip，端口自动随机分配
    //用于配置本服务器的ip和端口，”akka.actor.allow-java-serialization = "on"“表示使用java来序列化，远程发送消息需要经过序列化
    //注意：akka.actor.warn-about-java-serializer-usage = "off"这里忽略了java序列化的警告，使用java序列化性能差，不安全
    val config = ConfigFactory.parseString(
      s"""
         |akka.actor.provider = "akka.remote.RemoteActorRefProvider"
         |akka.actor.allow-java-serialization = "on"
         |akka.actor.warn-about-java-serializer-usage = "off"
         |akka.remote.artery.enable = "on"
         |akka.remote.artery.canonical.hostname = $host
         |akka.remote.artery.canonical.port = $port
         |""".stripMargin)
    val serverActorSystem = ActorSystem("Server", config) //“Server”指定的是ActorSystem的名字
    //“TextTalkServer”指定的是Actor的名字
    val chatServerActorRef: ActorRef = serverActorSystem.actorOf(Props[TextTalkServer], "TextTalkServer")
    val serverInfo = UserInfo("server", chatServerActorRef) //创建服务器信息的实例
    userInformation("server") = serverInfo //将自身的ActorRef先加入到userInformation表中，可以让其它用户向服务器发消息
    chatServerActorRef ! "start" //给自己发送消息，是初始化的一种方法
    breakable(
      while (true) {
        println("-" * 100)
        println("ls->查看用户表\tshutdown->关闭服务器")
        println("主机名(ActorRef) = TextTalkServer" + "\t" + "ActorSystem = Server" + "\n" +
          "ip = " + AddressExtension.hostOf(serverActorSystem) + "\t" +
          "端口 = " + AddressExtension.portOf(serverActorSystem))
        val order = StdIn.readLine() //接收输入
        order match { //根据输入的字符串判断指令做对应操作
          case "ls" => for ((k, v) <- userInformation) println(k + "\t" + v.userActorRef) //展示用户信息表
          case "shutdown" => //关闭服务器
            chatServerActorRef ! "shutdown"
            break()
          case user: String => //符合”@+用户名“的格式时，判断用户存在后发送消息
            if ("".equals(user)) println() //处理掉输入的空字符串
            else if (userInformation == null) println("userInformation = null，请尝试更新用户信息表（尝试“ls”命令）")
            else if ("@".equals(user.head.toString)) {
              if (userInformation.contains(user.tail)) {
                print("发送消息@" + user.tail + ": ")
                val mes = StdIn.readLine()
                userInformation(user.tail).userActorRef ! MessageProtocol("Server", mes)
              } else println("用户不存在或者您的输入有误，请重新输入！")
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
