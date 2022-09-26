/*
如果要创建更多用户，只需复制粘贴这里的所有代码，并将所有的uid1替换成uid2或uid3或……
最后修改ip和端口号即可
 */
package Chat.user

import Chat.common._
import akka.actor._
import com.typesafe.config.ConfigFactory
import scala.io.StdIn
import scala.util.control.Breaks.{break, breakable}

class uid1_Start  //用户独有的类，每个用户的Start类都不一样，用于自身的初始化

class uid1(serverHost: String, serverPort: Int) extends Actor {
  var serverActorRef: ActorSelection = _  //用于存放远程服务器的ActorRef

  override def preStart: Unit = {
    serverActorRef = context.actorSelection(
      s"akka://Server@$serverHost:$serverPort/user/TextTalkServer") //获取远程服务器的ActorRef
  }

  override def receive: Receive = {
    case _: uid1_Start =>
      serverActorRef ! UserInformation("uid1", uid1.selfActorRef) //用户上线第一时间把自身名称和ActorRef上传服务器
      println("uid1用户已上线！")
    case message: MessageProtocol =>  //接收发来的聊天消息
      println("\n" + message.user + "发来消息: " + message.message)
      print("uid1@" + uid1.uid1Host + ":" + uid1.uid1Port + "# ")
    case userMap: UserList => //一旦接收到用户信息表就会更新并打印全部用户信息
      uid1.userInformation = userMap.userInformation
      for ((k, v) <- uid1.userInformation) println(k + "\t" + v)
    case "ls" => serverActorRef ! UserList(uid1.userInformation)  //向服务器发送用户信息表
    case "shutdown" =>
      println("接收到shutdown指令，退出系统")
      serverActorRef ! Offline("uid1")  //下线前向服务器发送消息，删除本用户信息
      context.stop(self)  //这条语句和下面的语句用来退出akka
      context.system.terminate()
  }
}

object uid1 {
  var selfActorRef: ActorRef = _  //用于存放自己的ActorRef
  var userInformation: scala.collection.mutable.HashMap[String, ActorRef] = _ //用户名和对应的ActorRef的映射表
  //配置本用户ip和端口和远程服务器的ip和端口
  val (uid1Host, uid1Port, serverHost, serverPort) = ("127.0.0.1", 9990, "127.0.0.1", 9999)
  def main(args: Array[String]): Unit = {
    //用于配置本用户的ip和端口，”akka.actor.allow-java-serialization = "on"“表示使用java来序列化，远程发送消息需要经过序列化
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
        Thread.sleep(500) //延迟只是为了输出的格式好看，否则下面的Server@……#会和akka的信息不换行而叠在一起
        println("-" * 100)
        println("ls->查看/刷新用户表")
        print("uid1@" + uid1Host + ":" + uid1Port + "# ") //模仿Linux命令行界面
        val order = StdIn.readLine()  //接收输入
        order match { //根据输入的字符串判断指令做对应操作
          case "ls" =>  //获取，刷新，展示用户信息表
            selfActorRef ! "ls"
          case "shutdown" =>  //关机下线
            selfActorRef ! "shutdown"
            break()
          case user: String =>  //给用户发送消息
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
