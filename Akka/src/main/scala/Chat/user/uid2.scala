package Chat.user

import Chat.common._
import akka.actor._
import com.typesafe.config.ConfigFactory
import scala.io.StdIn
import scala.util.control.Breaks.{break, breakable}

class uid2_Start

class uid2(serverHost: String, serverPort: Int) extends Actor {
  var serverActorRef: ActorSelection = _

  override def preStart: Unit = {
    serverActorRef = context.actorSelection(
      s"akka://Server@$serverHost:$serverPort/user/TextTalkServer") //获取远程服务器的ActorRef
  }

  override def receive: Receive = {
    case _: uid2_Start =>
      serverActorRef ! UserInformation("uid2", uid2.selfActorRef) //用户上线第一时间把自身名称和ActorRef上传服务器
      println("uid2用户已上线！")
    case message: MessageProtocol =>
      println("\n" + message.user + "发来消息: " + message.message)
      print("uid2@" + uid2.uid2Host + ":" + uid2.uid2Port + "# ")
    case userMap: UserList =>
      uid2.userInformation = userMap.userInformation
      for ((k, v) <- uid2.userInformation) println(k + "\t" + v)
    case "ls" => serverActorRef ! UserList(uid2.userInformation)
    case "shutdown" =>
      println("接收到shutdown指令，退出系统")
      serverActorRef ! Offline("uid2")
      context.stop(self)
      context.system.terminate()
  }
}

object uid2 {
  var selfActorRef: ActorRef = _
  var userInformation: scala.collection.mutable.HashMap[String, ActorRef] = _ //用户名和对应的ActorRef的映射表
  val (uid2Host, uid2Port, serverHost, serverPort) = ("127.0.0.1", 9989, "127.0.0.1", 9999)
  def main(args: Array[String]): Unit = {
    val config = ConfigFactory.parseString(
      s"""
         |akka.actor.provider = "akka.remote.RemoteActorRefProvider"
         |akka.actor.allow-java-serialization = "on"
         |akka.remote.artery.enable = "on"
         |akka.remote.artery.canonical.hostname = $uid2Host
         |akka.remote.artery.canonical.port = $uid2Port
         |""".stripMargin)

    val uid2ActorSystem = ActorSystem("user", config)
    val uid2ActorRef: ActorRef = uid2ActorSystem.actorOf(Props(new uid2(serverHost, serverPort)), "uid2")
    selfActorRef = uid2ActorRef

    uid2ActorRef ! new uid2_Start
    breakable(
      while (true) {
        Thread.sleep(500)
        println("-" * 100)
        println("ls->查看/刷新用户表")
        print("uid2@" + uid2Host + ":" + uid2Port + "# ")
        val order = StdIn.readLine()
        order match {
          case "ls" =>
            selfActorRef ! "ls"
          case "shutdown" =>
            selfActorRef ! "shutdown"
            break()
          case user: String =>
            if (userInformation.contains(user)) {
              print("发送消息@" + user + ": ")
              val mes = StdIn.readLine()
              userInformation(user) ! MessageProtocol("uid2", mes)
            } else println("用户不存在或者您的输入有误，请重新输入！")
          case _ => println("没有匹配结果")
        }
      }
    )
  }
}
