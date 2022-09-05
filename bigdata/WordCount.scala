package bigdata

import scala.collection.mutable

object WordCount {
  def main(args: Array[String]): Unit = {
    def sum(n1: String, n2: String): String = {
      n1 + " " + n2
    }

    val word_Map = new mutable.HashMap[String, Int]

    def add(n1: String): Unit = {
      if (word_Map.contains(n1))
        word_Map(n1) += 1
      else
        word_Map(n1) = 1
    }

    val lines = List("atguigu han hello", "atguigu han aaa aaa aaa ccc ddd uuu")
    lines.reduceLeft(sum).split(" ").map(add)
    println(word_Map)
  }
}
