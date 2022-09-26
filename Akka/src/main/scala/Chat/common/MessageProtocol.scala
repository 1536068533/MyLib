package Chat.common

import akka.actor.ActorRef

case class UserInformation(user: String, userActorRef: ActorRef)  //用户上传自己的信息给服务器

case class MessageProtocol(user: String, message: String) //用于发送聊天消息

case class UserList(userInformation: scala.collection.mutable.HashMap[String, ActorRef])  //用户传递用户信息表

case class Offline(user: String)  //用于用户的下线操作，发送给服务器会删除对应用户的信息
