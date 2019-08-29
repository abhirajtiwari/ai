#include <iostream> 
#include <sys/stat.h> 
#include <fstream>
  
void writedata() 
{ 
    mkfifo("fifo", 0666);
	std::string file = "./fifo";
	std::ofstream output (file);
	output << "hello";
	output.close();
} 


int main() {
	while (1) {
			writedata();
	}
	return 0;
}
