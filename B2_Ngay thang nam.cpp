#include <iostream>
using namespace std;

int ld, tmpd, tmpm, tmpy;
void menu(int &d, int &m, int &y);

int CountMonth_LeapYear(int m, int y, int &ld) {
    bool LY = (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
    switch (m) {
        case 4: case 6: case 9: case 11:
            ld = 30;
            break;
        case 2:
            if (LY == false) ld = 28;
            else ld = 29;
            break;
    }
}

int check_date(int d, int m, int y) {
    if (d <= 0 || m <= 0 || y <= 0 || d > 31 || m > 12) {
        cout << "Ngay khong hop le";
        exit(0);
    }
    ld = 31;
    CountMonth_LeapYear(m, y, ld);
    if (d > ld) {
        cout << "Ngay khong hop le";
        exit(0);
    }
    cout << "Ngay hop le" << endl;
    menu(d, m, y);
}

void Tomorrow(int &d, int &m, int &y) {
    CountMonth_LeapYear(m, y, ld);
    tmpd = d;
    tmpm = m;
    tmpy = y;

    if (tmpd == ld) {
        tmpd = 1;
        if (tmpm == 12) {
            tmpm = 1;
            tmpy++;
        } else tmpm++;
    } else tmpd++;

    cout << "Ngay mai la: " << tmpd << "/" << tmpm << "/" << tmpy << endl;
}

void Yesterday(int &d, int &m, int &y) {
	tmpd = d;
    tmpm = m;
    tmpy = y;
    
	if(tmpd == 1){
		if(tmpm == 1){
			tmpm = 12;
			tmpy--;
		} else{
			tmpm--;
			CountMonth_LeapYear(tmpm, tmpy, ld);
			tmpd = ld;
		}
	} else tmpd--;
	
	cout << "Ngay hom qua la: " << tmpd << "/" << tmpm << "/" << tmpy << endl;
}

void DayofWeek(int &d, int &m, int &y){
	int dow;
	CountMonth_LeapYear(m, y, ld);
	tmpd = d;
    tmpm = m;
    tmpy = y;
	
	tmpy -= (14 - tmpm) / 12;
	tmpm += 12 * ((14 - tmpm) / 12 )- 2;
	dow = (tmpd + tmpy + tmpy / 4 - tmpy / 100 + tmpy / 400 + (31 * tmpm) / 12) % 7;
	cout << "Hom nay la ";
	if(!dow) cout << "Chu Nhat\n";
	else cout << "Thu " << dow+1 << "\n";
}

void DayofYear(int &d, int &m, int &y){
	int doy = 0;
	
	for(int mc = 1; mc < m; mc++){
		int ld;
		CountMonth_LeapYear(mc, y, ld);
		doy += ld;
	}
	doy += d;
	
	cout << "Hom nay la ngay thu " << doy << " trong nam\n";
}

void Numerology_Number(int &d, int &m, int &y){
	int sum, tmps, dg;
	tmpd = d;
    tmpm = m;
    tmpy = y;
    
    int dtA[] = {tmpd, tmpm, tmpy};
    
    for(int i = 0; i < 3; i++){
    	dg = dtA[i];
    	while(dg > 0){
    		sum += dg % 10;
    		dg /= 10;
		}
	}
	
	while (sum > 11){
		tmps = 0;
		while (sum > 0){
			tmps += sum % 10;
			sum /= 10;
		}
		sum = tmps;
	}
	
	cout << "Con so chu dao cua ban la: " << sum << endl;
}

void menu(int &d, int &m, int &y) {
	int slt;
    while (true) {
    	cout << "\nHom nay la: " << d << "/" << m << "/" << y << endl;
        cout << "---------- Menu ----------\n";
        cout << "1. Tim ngay mai\n";
        cout << "2. Tim ngay hom qua\n";
        cout << "3. Ngay thu may trong tuan\n";
        cout << "4. Ngay thu may trong nam\n";
        cout << "5. Con so chu dao\n";
        cout << "6. Exit\n";
        cout << "----------------------------\n";
        cout << "Select: ";
        cin >> slt;
        switch (slt) {
            case 1:
                Tomorrow(d, m, y);
                break;
            case 2:
                Yesterday(d, m, y);
                break;
            case 3:
                DayofWeek(d, m, y);
                break;
            case 4:
                DayofYear(d, m, y);
                break;
            case 5:
                Numerology_Number(d, m, y);
                break;
            case 6:
                cout << "Closing program.......";
                exit(0);
            default:
                cout << "Cannot find selected number. Please re-enter\n";
                break;
        }
    }
}

int main() {
    int d, m, y;
    cout << "Nhap ngay thang nam: ";
    cin >> d >> m >> y;
    check_date(d, m, y);
}