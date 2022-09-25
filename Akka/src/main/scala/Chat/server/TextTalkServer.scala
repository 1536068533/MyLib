package Chat.server

import Chat.common._
import akka.actor._
import com.typesafe.config.ConfigFactory

import scala.io.StdIn
import scala.util.control.Breaks.{break, breakable}

class TextTalkServer extends Actor {
  override def receive: Receive = {
    case "start" => println("start 聊天服务器开始工作了")
    case userData: UserInformation => TextTalkServer.userInformation(userData.user) = userData.userActorRef
    case _: UserList => sender() ! UserList(TextTalkServer.userInformation) //如果有人查询用户列表，则返回用户列表
    case message: MessageProtocol =>
      println("\n" + message.user + "发来消息: " + message.message)
      print("Server@" + TextTalkServer.host + ":" + TextTalkServer.port + "# ")
    case user: Offline => TextTalkServer.userInformation -= user.user
    case "shutdown" =>
      println("接收到shutdown指令，退出系统")
      context.stop(self)
      context.system.terminate()
  }
}

object TextTalkServer {
  val userInformation = new scala.collection.mutable.HashMap[String, ActorRef] //用户名和对应的ActorRef的映射表
  val host = "127.0.0.1"
  val port = 9999
  def main(args: Array[String]): Unit = {
    val config = ConfigFactory.parseString(
      s"""
         |akka.actor.provider = "akka.remote.RemoteActorRefProvider"
         |akka.actor.allow-java-serialization = "on"
         |akka.remote.artery.enable = "on"
         |akka.remote.artery.canonical.hostname = $host
         |akka.remote.artery.canonical.port = $port
         |""".stripMargin)
    val serverActorSystem = ActorSystem("Server", config)
    val chatServerActorRef: ActorRef = serverActorSystem.actorOf(Props[TextTalkServer], "TextTalkServer")
    userInformation("server") = chatServerActorRef
    chatServerActorRef ! "start"
    breakable(
      while (true) {
        Thread.sleep(500)
        println("-" * 100)
        println("ls->查看用户表\tshutdown->关闭服务器")
        print("Server@" + host + ":" + port + "# ")
        val order = StdIn.readLine()
        order match {
          case "ls" => for ((k, v) <- userInformation) println(k + "\t" + v)
          case "shutdown" =>
            chatServerActorRef ! "shutdown"
            break()
          case user: String =>
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
