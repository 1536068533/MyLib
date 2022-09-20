package Chat.user

import akka.actor._
import com.typesafe.config.ConfigFactory

class uid1(serverHost: String, serverPort: Int) extends Actor {
  var serverActorRef: ActorSelection = _

  override def preStart: Unit = {
    serverActorRef = context.actorSelection(
      s"akka.tcp://Server@$serverHost:$serverPort/user/TextTalkServer")
    println("serverActorRef=" + serverActorRef)
  }

  override def receive: Receive = {
    case "start" => println("uid1用户运行")
  }
}

object uid1 {
  def main(args: Array[String]): Unit = {
    val (uid1Host, uid1Port, serverHost, serverPort) = ("127.0.0.1", 9995, "127.0.0.1", 9999)
    val config = ConfigFactory.parseString(
      s"""
         |akka.actor.provider="akka.remote.RemoteActorRefProvider"
         |akka.remote.netty.tcp.hostname=$uid1Host
         |akka.remote.netty.tcp.port=$uid1Port
         |""".stripMargin)

    val uid1ActorSystem = ActorSystem("user", config)
    val uid1ActorRef: ActorRef = uid1ActorSystem.actorOf(Props(new uid1(serverHost, serverPort)),"uid1")

    uid1ActorRef ! "start"
  }
}
