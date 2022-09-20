package Chat.server

import akka.actor._
import com.typesafe.config.ConfigFactory

class TextTalkServer extends Actor {
  override def receive: Receive = {
    case "start" => println("start 聊天服务器开始工作了")
  }
}

object TextTalkServer {
  def main(args: Array[String]): Unit = {
    val host = "127.0.0.1"
    val port = 9999
    val config = ConfigFactory.parseString(
      s"""
         |akka.actor.provider="akka.remote.RemoteActorRefProvider"
         |akka.remote.netty.tcp.hostname=$host
         |akka.remote.netty.tcp.port=$port
         |""".stripMargin)

    val serverActorSystem = ActorSystem("Server", config)
    val chatServerActorRef: ActorRef = serverActorSystem.actorOf(Props[TextTalkServer], "TextTalkServer")

    chatServerActorRef ! "start"
  }
}
