#include <stdio.h>

int main(){
	float toan,ly,hoa,tb;
	printf("Nhap diem Toan: ");
	scanf("%f",&toan);
	printf("Nhap diem Ly: ");
	scanf("%f",&ly);
	printf("Nhap diem Hoa: ");
	scanf("%f",&hoa);
	if((toan>=0 && toan<=10) && (ly>=0 && ly<=10) && (hoa>=0 && hoa<=10)){
		tb = (toan+ly+hoa)/3;
		if(tb>=8){
		printf("Diem trung binh la %.2f\nXep loai hoc luc: Gioi",tb);
		}
		if(tb<8 && tb>=6.5){
			printf("Diem trung binh la %.2f\nXep loai hoc luc: Kha",tb);
		}
		if(tb<6.5 && tb>=5){
			printf("Diem trung binh la %.2f\nXep loai hoc luc: Trung binh",tb);
		}
		if(tb<5){
			printf("Diem trung binh la %.2f\nXep loai hoc luc: Yeu",tb);
		}
	}
	else{
		printf("Co diem so khong hop le");
	}
}
