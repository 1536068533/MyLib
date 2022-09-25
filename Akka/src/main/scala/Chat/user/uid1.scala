package Chat.user

import Chat.common._
import akka.actor._
import com.typesafe.config.ConfigFactory
import scala.io.StdIn
import scala.util.control.Breaks.{break, breakable}

class uid1_Start

class uid1(serverHost: String, serverPort: Int) extends Actor {
  var serverActorRef: ActorSelection = _

  override def preStart: Unit = {
    serverActorRef = context.actorSelection(
      s"akka://Server@$serverHost:$serverPort/user/TextTalkServer") //获取远程服务器的ActorRef
  }

  override def receive: Receive = {
    case _: uid1_Start =>
      serverActorRef ! UserInformation("uid1", uid1.selfActorRef) //用户上线第一时间把自身名称和ActorRef上传服务器
      println("uid1用户已上线！")
    case message: MessageProtocol =>
      println("\n" + message.user + "发来消息: " + message.message)
      print("uid1@" + uid1.uid1Host + ":" + uid1.uid1Port + "# ")
    case userMap: UserList =>
      uid1.userInformation = userMap.userInformation
      for ((k, v) <- uid1.userInformation) println(k + "\t" + v)
    case "ls" => serverActorRef ! UserList(uid1.userInformation)
    case "shutdown" =>
      println("接收到shutdown指令，退出系统")
      serverActorRef ! Offline("uid1")
      context.stop(self)
      context.system.terminate()
  }
}

object uid1 {
  var selfActorRef: ActorRef = _
  var userInformation: scala.collection.mutable.HashMap[String, ActorRef] = _ //用户名和对应的ActorRef的映射表
  val (uid1Host, uid1Port, serverHost, serverPort) = ("127.0.0.1", 9990, "127.0.0.1", 9999)
  def main(args: Array[String]): Unit = {
    val config = ConfigFactory.parseString(
      s"""
         |akka.actor.provider = "akka.remote.RemoteActorRefProvider"
         |akka.actor.allow-java-serialization = "on"
         |akka.remote.artery.enable = "on"
         |akka.remote.artery.canonical.hostname = $uid1Host
         |akka.remote.artery.canonical.port = $uid1Port
         |""".stripMargin)

    val uid1ActorSystem = ActorSystem("user", config)
    val uid1ActorRef: ActorRef = uid1ActorSystem.actorOf(Props(new uid1(serverHost, serverPort)), "uid1")
    selfActorRef = uid1ActorRef

    uid1ActorRef ! new uid1_Start
    breakable(
      while (true) {
        Thread.sleep(500)
        println("-" * 100)
        println("ls->查看/刷新用户表")
        print("uid1@" + uid1Host + ":" + uid1Port + "# ")
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
              userInformation(user) ! MessageProtocol("uid1", mes)
            } else println("用户不存在或者您的输入有误，请重新输入！")
          case _ => println("没有匹配结果")
        }
      }
    )
  }
}
