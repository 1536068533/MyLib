package Chat.common

import akka.actor.ActorRef

case class RegisterUser(userName: String, userActorRef: ActorRef) //用于用户注册，用户上传自己的信息给服务器

case class RegisteredUser(reply: Boolean) //服务器用来反馈是否注册成功

case class MessageProtocol(user: String, message: String) //用于发送聊天消息

case object UserList //用户请求获取服务器的用户信息表

case class UserList(userInformation: scala.collection.mutable.HashMap[String, ActorRef]) //服务器下发用户信息表

case class Offline(user: String) //用于用户的下线操作，发送给服务器会删除对应用户的信息

//用来保存到服务器的管理用户信息的Map映射表，可在这里进行扩展（如增加客户端上一次心跳的时间）
class BeatInformation(user: String, userActorRef: ActorRef)
