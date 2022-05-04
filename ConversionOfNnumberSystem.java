package Interest;
import java.util.Scanner;
public class ConversionOfNnumberSystem {//conversion of number system进制转换
	public static void main(String args[]) {
		Scanner input=new Scanner(System.in); 
		System.out.println("您接下来要输入的数的进制是？（请输入2或8或10或16）");
		int x=input.nextInt();
		if(x==2) {
			System.out.print("请输入数值：");
			double a=input.nextDouble();
			int integer=(int)a;//integer整数，这行用来取输入的数的整数部分
			String decimalString=String.valueOf(a).substring(String.valueOf(integer).length()+1);
			int decimal=Integer.valueOf(decimalString);//decimal小数，这行和上一行用来获取小数部分，注意会漏掉前面的0
			int addInteger=0,multiplicative=1;
			int integerCopy=integer;
			for(int circulation=1;circulation<=String.valueOf(integer).length();circulation++) {//circulation循环
				addInteger=(int) (integerCopy%10)*multiplicative+addInteger;
				integerCopy=integerCopy/10;
				multiplicative=multiplicative*2;
			}
			int decimalCopy=decimal,addDecimal=0;
			multiplicative=1/2;
			if(decimalString.length()!=String.valueOf(decimal).length()) {
				for(int circulation=decimalString.length()-String.valueOf(decimal).length();circulation>0;circulation--) {
					multiplicative/=2;
				}
			}
			for(int circulation=String.valueOf(decimal).length();circulation>0;circulation--) {
				for(circulation=String.valueOf(decimal).length()+1;circulation>0;circulation--) {
					decimalCopy/=10;
				}
				addDecimal=((int)decimalCopy)*multiplicative+addDecimal;
				multiplicative/=2;
				System.out.println(1);
			}
			System.out.println("十进制："+addInteger+"."+addDecimal);
		}
	}
}
