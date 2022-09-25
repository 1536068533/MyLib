package Chat.common

import akka.actor.ActorRef

case class UserInformation(user: String, userActorRef: ActorRef)

case class MessageProtocol(user: String, message: String)

case class UserList(userInformation: scala.collection.mutable.HashMap[String, ActorRef])

case class Offline(user: String)
