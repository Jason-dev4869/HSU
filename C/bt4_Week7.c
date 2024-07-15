#include <stdio.h>

int main(){
	float kwh, tt;
	printf("Nhap so KWh: ");
	scanf("%d", kwh);
	if(kwh > 0 && kwh <=100){
		tt=kwh*1000;
	}
	if(kwh>100&&kwh<=150){
		tt=(kwh-100)*1200+100000;
	}
	if(kwh>150&&kwh<=200){
		tt=(kwh-150)*1600+(kwh-100)*1200+100000;
	}
	else{
		tt=(kwh-200)*2000+(kwh-150)*1600+(kwh-100)*1200+100000
	}
}
