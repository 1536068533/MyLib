package com.example.study;

import java.io.File;
import java.io.Serial;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
/*
将路径“H:\计算机类\MySQL\视频”上的文件名全部重命名，例如↓
文件名：
“MySQL数据库入门到大牛，mysql安装到优化，百科全书级，全网天花板 - 1.01-MySQL教程简介.mp4”
重命名为：
“01-MySQL教程简介.mp4”

如果重命名失败则抛出异常
 */
public class FileRename {
    public static void main(String[] args) {
        //初始化
        File file_dir = new File("H:\\计算机类\\MySQL\\视频");
        String[] file_list = file_dir.list();

        //开始处理
        if (file_list != null) {
            String file_name;

            for (String s : file_list){
                File file = new File(file_dir,s);//原文件绝对路径
                // 编译正则表达式
                Pattern pattern = Pattern.compile("\\d{1,3}-.+\\(");
                // 创建匹配器
                Matcher matcher = pattern.matcher(s);
                // 查找匹配的子串
                boolean found = matcher.find();

                // 输出结果
                if (found) {
                    file_name = matcher.group().substring(0, matcher.group().length() - 1)+".mp4";
                    System.out.println("找到匹配的子串: " + file_name);
                    File output_file = new File(file_dir,file_name);
                    if(file.renameTo(output_file)){
                        System.out.println("改名成功");
                    }else{
                        try{
                            throw new RenameFail("改名失败！！！" + file_name);
                        }catch(RenameFail e){
                            e.printStackTrace();
                        }
                    }
                } else {
                    System.out.println("没有找到匹配的子串");
                }
            }
        }
    }
}

class RenameFail extends Exception{
    @Serial
    private static final long serialVersionUID = 143242342323L;

    public RenameFail(String message){
        super(message);
    }
}
