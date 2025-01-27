#include <stdio.h>

int tong(int a, int b);
int hieu(int a, int b);
int nhan(int a, int b);
int chia(int a, int b);
int max(int a, int b);
int uscln(int a, int b);
int bcnn (int a, int b);

int main()
{

	int n1,n2;
	int chon;

	printf("Nhap so thu 1:");
	scanf("%d",&n1);
	printf("Nhap so thu 2:");
	scanf("%d",&n2);
	do{
		printf("\n---------MENU---------");
		printf("\n(1.) Tong 2 so");
		printf("\n(2.) Hieu 2 so");
		printf("\n(3.) Thuong 2 so");
		printf("\n(4.) Tich 2 so");
		printf("\n(5.) Max 2 so");
		printf("\n(6.) USCLN 2 so");
		printf("\n(7.) BCNN 2 so");
		printf("\n(8.) Thoat chuong trinh");
		printf("\nNhap vao chon lua cua ban:");
		scanf("%d",&chon);
		switch(chon)
		{
			case 1:	
			{
				tong(n1,n2);
				break;
			}
			case 2:	
			{
				hieu(n1,n2);
				break;
			}
			case 3:	
			{
				chia(n1,n2);
				break;
			}
			case 4:	
			{
				nhan(n1,n2);
				break;
			}
			case 5:	
			{
				max(n1,n2);
				break;
			}
			case 6:	
			{
				uscln(n1,n2);
				break;
			}
			case 7:	
			{
				bcnn(n1,n2);
				break;
			}
			case 8:	
			{
				printf("Closing...");
				break;
			}
			default:
				{
					printf("\nnhap sai!nhap lai de!");
				}
		}
	}while(chon!=8);
}

int tong(int a, int b){
	printf("\n%d+%d=%d",a,b,a+b);
}

int hieu(int a, int b){
	printf("\n%d-%d=%d",a,b,a-b);
}

int chia(int a, int b){
	printf("\n%d/%d=%.2f",a,b,a/b);
}

int nhan(int a, int b){
	printf("\n%d*%d=%d",a,b,a*b);
}

int max(int a, int b){
	int m=0;
	m=(a>b)?a:b;
	printf("\nSo lon nhat giua hai so la: %d",m);
}

int uscln(int a, int b){
	while ( a != b)
    {
        if (a > b){
        	a = a - b;
            printf("\nUSCLN: %d",a);
            return a;
		}
        else{
        	b = b - a;
            printf("\nUSCLN: %d",b);
            return b;
		}
    }
} 

int bcnn(int a, int b){
	int result = uscln(a, b);
	printf("\tBCNN: %d",a*b/result);
}
