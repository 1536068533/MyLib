package Interest;
import java.util.Scanner;
public class ConversionOfNnumberSystem {//conversion of number system����ת��
	public static void main(String args[]) {
		Scanner input=new Scanner(System.in); 
		System.out.println("��������Ҫ��������Ľ����ǣ���������2��8��10��16��");
		int x=input.nextInt();
		if(x==2) {
			System.out.print("��������ֵ��");
			double a=input.nextDouble();
			int integer=(int)a;//integer��������������ȡ�����������������
			String decimalString=String.valueOf(a).substring(String.valueOf(integer).length()+1);
			int decimal=Integer.valueOf(decimalString);//decimalС�������к���һ��������ȡС�����֣�ע���©��ǰ���0
			int addInteger=0,multiplicative=1;
			int integerCopy=integer;
			for(int circulation=1;circulation<=String.valueOf(integer).length();circulation++) {//circulationѭ��
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
			System.out.println("ʮ���ƣ�"+addInteger+"."+addDecimal);
		}
	}
}
