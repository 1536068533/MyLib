package Chat.common

import akka.actor.ActorRef

case class RegisterUser(userName: String, userActorRef: ActorRef) //用于用户注册，用户上传自己的信息给服务器

case class RegisteredUser(reply: Any) //服务器用来反馈是否注册成功

case class MessageProtocol(user: String, message: String) //用于发送聊天消息

case object UserList //用户请求获取服务器的用户信息表

case class UserList(userInformation: scala.collection.mutable.HashMap[String, UserInfo]) //服务器下发用户信息表

case class Offline(user: String) //用于用户的下线操作，发送给服务器会删除对应用户的信息

case object SendHeartBeat //每隔一段时间由定时器发给自己的消息

case class HeartBeat(userName: String) //每隔一段时间由定时器触发，而向服务器发送的心跳消息

case class UserInfo(userName: String, userActorRef: ActorRef){
  /*
  这个类用来保存到服务器的用户信息映射表中，这里还可以扩展更多功能（比如增加上一次心跳的时间）
   */
  var lastHeartBeat: Long = System.currentTimeMillis() //记录最近一次发送心跳的时间
}

case object StartTimeOutUser //服务器给自己发送一个触发检查超时user的信息

case object RemoveTimeOutUser //服务器给自己发消息，移除用户信息表中心跳超时的user

case object CheckConnect //用户给自己消息，检查与服务器的连接是否正常