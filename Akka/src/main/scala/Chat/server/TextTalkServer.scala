package Chat.server

import Chat.common._
import akka.actor._
import com.typesafe.config.ConfigFactory
import scala.io.StdIn
import scala.util.control.Breaks.{break, breakable}

class TextTalkServer extends Actor {
  override def receive: Receive = {
    case "start" => println("start 聊天服务器开始工作了") //可以用于初始化，做一些准备工作
    case userData: RegisterUser =>
      //用户名已存在，向用户答复注册失败，否则，加入用户信息表并向用户答复注册成功
      if (TextTalkServer.userInformation.contains(userData.userName)) sender() ! RegisteredUser(false)
      else{
        TextTalkServer.userInformation(userData.userName) = userData.userActorRef
        sender() ! RegisteredUser(true)
      }
    case UserList => sender() ! UserList(TextTalkServer.userInformation) //如果有人查询用户列表，则返回用户列表
    case message: MessageProtocol => println(message.user + "发来消息: " + message.message)
    case user: Offline => TextTalkServer.userInformation -= user.user
    case "shutdown" =>
      println("接收到shutdown指令，退出系统")
      context.stop(self) //这条语句和下面的语句用来退出akka
      context.system.terminate()
  }
}

object TextTalkServer {
  val userInformation = new scala.collection.mutable.HashMap[String, ActorRef] //用户名和对应的ActorRef的映射表
  def main(args: Array[String]): Unit = {
    val (host, port) = (args(0), 9999) //指定本服务器的ip和端口
    //用于配置本服务器的ip和端口，”akka.actor.allow-java-serialization = "on"“表示使用java来序列化，远程发送消息需要经过序列化
    val config = ConfigFactory.parseString(
      s"""
         |akka.actor.provider = "akka.remote.RemoteActorRefProvider"
         |akka.actor.allow-java-serialization = "on"
         |akka.remote.artery.enable = "on"
         |akka.remote.artery.canonical.hostname = $host
         |akka.remote.artery.canonical.port = $port
         |""".stripMargin)
    val serverActorSystem = ActorSystem("Server", config) //“Server”指定的是ActorSystem的名字
    //“TextTalkServer”指定的是Actor的名字
    val chatServerActorRef: ActorRef = serverActorSystem.actorOf(Props[TextTalkServer], "TextTalkServer")
    userInformation("server") = chatServerActorRef //将自身的ActorRef先加入到userInformation表中，可以让其它用户向服务器发消息
    chatServerActorRef ! "start" //给自己发送消息，是初始化的一种方法
    breakable(
      while (true) {
        println("-" * 100)
        println("ls->查看用户表\tshutdown->关闭服务器")
        val order = StdIn.readLine() //接收输入
        order match { //根据输入的字符串判断指令做对应操作
          case "ls" => for ((k, v) <- userInformation) println(k + "\t" + v) //展示用户信息表
          case "shutdown" => //关闭服务器
            chatServerActorRef ! "shutdown"
            break()
          case user: String => //给用户发送消息
            if (userInformation.contains(user)) {
              print("发送消息@" + user + ": ")
              val mes = StdIn.readLine()
              userInformation(user) ! MessageProtocol("Server", mes)
            } else println("用户不存在或者您的输入有误，请重新输入！")
          case _ => println("没有匹配结果")
        }
      }
    )
  }
}
