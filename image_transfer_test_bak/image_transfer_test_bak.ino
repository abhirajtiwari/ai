void setup() {
  Serial.begin(9600);
}

uint8_t image[1556] = {37, 42, 165, 167, 165, 162, 161, 162, 163, 164, 166, 169, 170, 167, 165, 165, 166, 167, 167, 167, 166, 162, 160, 162, 168, 172, 173, 173, 171, 171, 174, 177, 177, 177, 177, 180, 181, 179, 178, 178, 178, 177, 176, 177, 163, 164, 162, 159, 159, 160, 161, 162, 165, 167, 167, 166, 165, 166, 168, 170, 170, 169, 167, 164, 163, 165, 169, 174, 177, 178, 177, 175, 175, 176, 174, 173, 175, 178, 180, 180, 181, 180, 177, 174, 172, 171, 158, 161, 160, 159, 159, 160, 161, 163, 165, 167, 167, 168, 169, 171, 173, 174, 174, 172, 169, 166, 165, 167, 169, 172, 175, 178, 178, 177, 177, 175, 174, 174, 176, 178, 179, 179, 179, 179, 176, 172, 169, 168, 156, 158, 159, 159, 159, 160, 163, 165, 167, 169, 171, 172, 173, 174, 176, 177, 175, 173, 170, 166, 165, 167, 169, 170, 173, 176, 178, 178, 178, 178, 177, 177, 178, 179, 177, 176, 176, 177, 176, 173, 169, 168, 159, 159, 160, 161, 162, 163, 164, 166, 169, 171, 172, 174, 175, 176, 177, 178, 177, 175, 171, 167, 166, 168, 172, 174, 175, 176, 177, 177, 178, 178, 179, 180, 180, 178, 177, 175, 174, 173, 173, 172, 170, 169, 165, 164, 165, 167, 167, 167, 168, 168, 169, 170, 172, 174, 176, 177, 178, 179, 179, 178, 175, 171, 169, 172, 177, 179, 179, 178, 178, 178, 179, 179, 180, 181, 180, 179, 178, 176, 173, 172, 171, 171, 170, 170, 173, 171, 173, 175, 175, 173, 172, 170, 168, 169, 171, 172, 174, 177, 178, 179, 181, 181, 180, 176, 174, 176, 180, 182, 182, 181, 181, 181, 181, 180, 181, 181, 181, 181, 180, 178, 176, 174, 174, 173, 174, 174, 176, 175, 176, 179, 179, 177, 175, 173, 172, 172, 172, 172, 173, 176, 179, 180, 181, 182, 182, 180, 178, 179, 182, 183, 182, 182, 182, 182, 181, 181, 181, 182, 183, 183, 183, 182, 181, 180, 179, 178, 178, 179, 178, 177, 178, 180, 180, 178, 177, 176, 176, 177, 176, 176, 177, 179, 181, 182, 182, 182, 183, 182, 181, 182, 185, 185, 183, 182, 183, 183, 182, 181, 182, 183, 183, 183, 183, 183, 184, 185, 184, 182, 181, 181, 179, 179, 179, 180, 180, 180, 179, 179, 180, 181, 182, 182, 182, 184, 183, 183, 183, 184, 183, 184, 184, 186, 187, 186, 183, 183, 183, 183, 183, 183, 183, 183, 183, 183, 182, 182, 183, 184, 183, 181, 181, 182, 180, 181, 182, 182, 181, 181, 181, 182, 182, 183, 184, 185, 186, 186, 184, 184, 184, 185, 185, 186, 186, 186, 187, 186, 185, 184, 183, 184, 184, 184, 184, 184, 184, 183, 182, 180, 181, 181, 181, 179, 180, 181, 182, 183, 184, 184, 183, 183, 184, 184, 184, 184, 184, 185, 186, 186, 185, 185, 184, 185, 186, 188, 188, 189, 189, 189, 188, 187, 186, 185, 185, 186, 186, 186, 186, 185, 183, 180, 179, 179, 178, 178, 179, 181, 184, 185, 185, 185, 185, 185, 186, 186, 185, 185, 184, 185, 186, 186, 184, 183, 183, 184, 186, 189, 191, 193, 194, 195, 195, 193, 190, 188, 187, 186, 186, 187, 187, 186, 184, 181, 179, 178, 178, 178, 180, 182, 185, 185, 185, 185, 186, 186, 186, 185, 185, 185, 184, 184, 185, 184, 181, 179, 179, 182, 185, 189, 192, 195, 198, 200, 200, 200, 197, 193, 189, 188, 187, 188, 187, 186, 184, 182, 180, 179, 179, 180, 181, 182, 184, 183, 183, 184, 185, 185, 185, 184, 184, 184, 184, 183, 182, 179, 175, 173, 175, 179, 184, 188, 191, 196, 199, 201, 203, 205, 204, 200, 195, 191, 189, 189, 187, 185, 182, 181, 179, 180, 181, 181, 181, 182, 181, 180, 180, 182, 184, 184, 184, 184, 184, 184, 183, 182, 178, 171, 167, 169, 173, 178, 182, 187, 191, 195, 199, 203, 207, 211, 211, 208, 203, 197, 191, 188, 184, 182, 180, 178, 178, 178, 180, 179, 179, 180, 179, 178, 179, 182, 184, 185, 185, 186, 185, 185, 184, 180, 171, 163, 161, 166, 172, 177, 181, 185, 191, 196, 202, 207, 211, 214, 214, 214, 211, 204, 195, 187, 182, 180, 179, 177, 176, 177, 177, 178, 177, 178, 180, 179, 180, 183, 185, 185, 185, 186, 185, 185, 183, 176, 163, 156, 158, 164, 170, 174, 179, 184, 192, 200, 206, 209, 211, 211, 211, 214, 217, 212, 201, 189, 181, 179, 179, 178, 178, 178, 178, 178, 179, 179, 179, 180, 181, 182, 184, 185, 184, 184, 183, 183, 181, 170, 157, 151, 155, 163, 169, 174, 178, 186, 76, 205, 207, 206, 205, 206, 206, 209, 214, 214, 206, 192, 182, 178, 179, 180, 181, 182, 182, 181, 182, 183, 177, 177, 178, 180, 182, 183, 182, 181, 181, 181, 177, 165, 151, 148, 153, 161, 168, 172, 178, 76, 76, 76, 202, 200, 200, 202, 202, 204, 206, 209, 205, 195, 182, 176, 177, 179, 182, 184, 185, 184, 183, 184, 175, 175, 175, 177, 179, 181, 181, 180, 180, 179, 173, 160, 147, 144, 150, 158, 165, 170, 76, 76, 76, 76, 76, 195, 197, 199, 200, 200, 201, 202, 201, 194, 183, 176, 175, 174, 175, 180, 184, 184, 183, 181, 174, 174, 175, 175, 177, 180, 181, 180, 180, 178, 171, 156, 143, 140, 147, 155, 161, 167, 176, 76, 76, 76, 191, 192, 194, 196, 198, 197, 197, 197, 198, 194, 184, 176, 173, 171, 169, 172, 179, 182, 182, 180, 173, 173, 173, 174, 176, 178, 179, 179, 178, 176, 169, 154, 139, 136, 143, 152, 159, 166, 176, 186, 76, 187, 188, 189, 191, 194, 195, 195, 195, 196, 197, 194, 186, 179, 176, 173, 171, 172, 177, 181, 180, 177, 171, 171, 171, 172, 174, 176, 176, 175, 174, 172, 166, 152, 137, 132, 137, 146, 155, 164, 175, 183, 184, 183, 184, 187, 189, 191, 193, 193, 193, 194, 195, 192, 187, 181, 179, 178, 177, 177, 179, 180, 179, 177, 169, 168, 168, 169, 172, 173, 173, 172, 170, 169, 163, 151, 135, 127, 131, 140, 150, 160, 171, 177, 178, 178, 181, 184, 187, 189, 190, 190, 190, 191, 191, 188, 182, 178, 177, 177, 177, 178, 178, 178, 177, 176, 168, 167, 166, 167, 169, 171, 171, 171, 170, 167, 164, 153, 137, 125, 126, 134, 144, 155, 166, 171, 172, 174, 178, 181, 184, 186, 187, 186, 187, 186, 184, 179, 172, 169, 168, 168, 169, 170, 171, 171, 171, 171, 169, 169, 168, 168, 169, 170, 171, 172, 171, 170, 168, 160, 145, 128, 122, 127, 137, 147, 157, 162, 165, 169, 174, 177, 179, 181, 182, 182, 182, 183, 178, 172, 166, 163, 162, 160, 161, 162, 161, 161, 161, 161, 170, 171, 170, 169, 170, 171, 171, 171, 171, 171, 171, 167, 155, 135, 121, 120, 127, 136, 146, 152, 156, 162, 168, 171, 173, 175, 176, 177, 178, 176, 172, 167, 166, 166, 163, 161, 161, 160, 158, 155, 153, 151, 168, 169, 168, 167, 167, 167, 167, 166, 165, 165, 166, 166, 158, 139, 120, 110, 113, 121, 130, 139, 147, 154, 159, 163, 166, 168, 170, 172, 171, 167, 163, 163, 167, 169, 166, 164, 163, 161, 158, 154, 149, 146, 159, 160, 158, 157, 156, 158, 159, 158, 156, 155, 154, 152, 146, 132, 115, 102, 100, 108, 118, 128, 136, 143, 150, 155, 158, 162, 164, 165, 162, 157, 155, 160, 166, 168, 167, 165, 164, 160, 155, 152, 150, 150, 149, 150, 148, 146, 145, 147, 148, 147, 147, 146, 140, 134, 129, 123, 113, 101, 100, 108, 119, 127, 132, 136, 142, 149, 153, 155, 157, 158, 155, 151, 153, 159, 163, 165, 165, 166, 165, 161, 156, 153, 155, 161, 142, 144, 145, 142, 141, 141, 140, 139, 141, 143, 136, 129, 127, 128, 124, 117, 117, 126, 136, 140, 141, 140, 144, 149, 150, 148, 151, 156, 157, 155, 157, 161, 163, 164, 165, 166, 168, 167, 162, 159, 163, 170, 142, 146, 149, 147, 145, 144, 142, 142, 144, 146, 144, 141, 143, 146, 145, 141, 143, 149, 155, 157, 155, 152, 152, 153, 150, 148, 153, 161, 165, 163, 164, 167, 168, 169, 169, 169, 170, 171, 169, 167, 169, 172, 146, 152, 155, 155, 153, 152, 151, 152, 155, 157, 157, 157, 160, 161, 159, 157, 160, 164, 166, 165, 163, 161, 160, 159, 156, 156, 162, 170, 173, 171, 171, 174, 176, 176, 175, 173, 173, 173, 173, 172, 172, 171, 149, 156, 159, 159, 159, 159, 159, 160, 162, 165, 166, 166, 168, 168, 166, 164, 166, 169, 169, 168, 167, 166, 165, 166, 165, 166, 171, 176, 177, 177, 177, 178, 180, 181, 180, 177, 175, 174, 175, 175, 173, 171, 149, 156, 160, 162, 163, 166, 165, 164, 164, 166, 167, 169, 171, 172, 170, 168, 169, 170, 171, 172, 171, 170, 171, 172, 173, 174, 176, 178, 179, 179, 180, 180, 180, 181, 180, 179, 177, 176, 176, 177, 176, 174, 152, 157, 162, 165, 169, 171, 171, 168, 166, 166, 167, 170, 173, 174, 173, 172, 172, 174, 175, 175, 175, 175, 176, 177, 178, 178, 178, 178, 179, 180, 180, 179, 179, 180, 180, 180, 178, 178, 178, 178, 178, 177 };

int count = 0;
void loop() {
  //while (count<307200 ) {
  if (count <= 0) {
  for (int i=0; i <1556; ++i){
      //Serial.print(image[i]);
      Serial.write(image[i]);
  } 
   // Serial.print("255");
   count++;
  }
}