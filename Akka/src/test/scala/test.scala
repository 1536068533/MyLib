import scala.io.StdIn

object test {
  def main(args: Array[String]): Unit ={
    val message = StdIn.readLine()
    println(message.head)
    println(message.tail)
  }
}
