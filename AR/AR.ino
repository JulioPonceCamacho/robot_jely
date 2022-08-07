#define brazoD2 2
#define brazoD1 3
#define brazoI2 4
#define brazoI1 5
#define ruedaD2 6
#define ruedaD1 7
#define ruedaI2 8
#define ruedaI1 9
#define TREG 11
#define ECHO 10
#define VCC 12
#define luz 13
int DURACION;     int DISTANCIA;   int accion;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(1,OUTPUT);
  digitalWrite(1,HIGH);
  pinMode(ruedaI1,OUTPUT);
  pinMode(ruedaI2,OUTPUT);
  pinMode(ruedaD1,OUTPUT);
  pinMode(ruedaD2,OUTPUT);
  pinMode(brazoI1,OUTPUT);
  pinMode(brazoI2,OUTPUT);
  pinMode(brazoD1,OUTPUT);
  pinMode(brazoD2,OUTPUT);
  pinMode(TREG,OUTPUT);
  pinMode(ECHO,INPUT);
  pinMode(VCC,OUTPUT);
  digitalWrite(VCC,HIGH);
  pinMode(luz,OUTPUT);
}

void loop() {
  sensor();
  if (Serial.available()>0){
    accion = Serial.read();
    switch(accion){
      case 'A':
        adelante();
        break;
      case 'D':
        detener();
        break;
      case 'O':
        atras();
        break;
      case 'L':
        giro_izquierda();
        break;
      case 'R':
        giro_derecha();
        break;
      case 'b':
        giro_izquierdaP();
        break;
      case 'v':
        giro_derechaP();
        break;
      case 'X':
        giro_izquierda_total(); 
        break;
      case 'Y':
        giro_derecha_total();
        break;
      case 'Z':
        luz_on();
        break;
      case 'P':
        luz_off();
        break;
      case 'T':
        pensar();
        break;
      case 't':
        pensar();
        break;
      case 'r':
        derecha();
        break;
      case 'l':
        izquierda();
        break;
      case 'H':
        parpadeo();
        break;
      case 'a':
        avanza();
        break;
      case 'n':
        aqui();
        break;
      case 'U':
        arriba();
        break;
      case 'Q':
        derechaBA();
        break;
      case 'q':
        derechaBR();
        break;
      case '-':
        derechaBAP();
        break;
      case '_':
        izquierdaBAP();
        break;
      case 'W':
        izquierdaBA();
        break;
      case 'w':
        izquierdaBR();
        break;
      case '1':
      Serial.println("Opcion: 1");
      delay(1000);
        parpadeo();
      delay(100);
      arriba();
      break;
      case '4':
        Serial.println("Opcion: 4");
        delay(1000);
        giro_izquierda();
        delay(100);
        atras();
        delay(100);
        derechaBA();
        delay(100);
        izquierdaBR();
        delay(100);
      break;
      case '5':
        Serial.println("Opcion: 5");
        delay(1000);
        giro_derecha();
        delay(100);
        atras();
        delay(100);
        derechaBA();
        delay(100);
        izquierdaBR();
        delay(100);
      break;
      case '6':
        Serial.println("Opcion: 6");
        delay(1000);
        aqui();
      break;
      case '7':
        Serial.println("Opcion: 7");
        delay(1000);
        derechaBA();
        delay(100);
        izquierdaBA();
        delay(100);
      break;
      case '8':
        Serial.println("Opcion: 8");
        delay(1000);
        derechaBR();
        delay(100);
        izquierdaBR();
        delay(100);
      break;
      case '9':
        Serial.println("Opcion: 9");
        delay(1000);
        giro_izquierda_total();
        delay(100);
      break;
      case '2':
        Serial.println("Opcion: 10");
        delay(1000);
        giro_derecha_total();
        delay(100);
      break;
       case '3':
        Serial.println("Opcion: 11");
        delay(1000);
        adelante();
        delay(100);
      break;
      case '0':
        Serial.println("Opcion: 12");
        delay(1000);
        atras();
        delay(100);
      break;
       case '.':
        Serial.println("Opcion: 13");
        delay(1000);
        izquierda();
        delay(100);
        derechaBA();
        delay(100);
        izquierdaBR();
        delay(100);
      break;
      case ':':
        Serial.println("Opcion: 14");
        delay(1000);
        derecha();
        delay(100);
        derechaBA();
        delay(100);
        izquierdaBR();
        delay(100);
        break;
    }
  }
}
void arriba(){
  moverBD();
  moverBI();
  delay(500);
  regresarBD();
  regresarBI();
  delay(500);
  detener(brazoD2,brazoD1);
  detener(brazoI2,brazoI1);
}

bool sensor(){
  bool parar=false;
  delay(120);
  digitalWrite(TREG,HIGH);
  delay(1);
  digitalWrite(TREG,LOW);
  DURACION=pulseIn(ECHO,HIGH);
  DISTANCIA=DURACION/58.2;
 if(DISTANCIA<8 && DISTANCIA>0){
    digitalWrite(ruedaI1,LOW);
    digitalWrite(ruedaI2,HIGH);
    digitalWrite(ruedaD1,LOW);
    digitalWrite(ruedaD2,HIGH);
    delay(500);
    detener();
    parar=true;
  }
  return parar;
}
void derechaBA(){
  moverBD();
  delay(400);
  detener(brazoD2,brazoD1);
}
void derechaBAP(){
  moverBD();
  delay(400);
  detener(brazoD2,brazoD1);
}
void izquierdaBA(){
  moverBI();
  delay(400);
  detener(brazoI2,brazoI1);
}
void izquierdaBAP(){
  moverBI();
  delay(50);
  detener(brazoI2,brazoI1);
}
void derechaBR(){
  regresarBD();
  sensor(); delay(50);
  detener(brazoD2,brazoD1);
}

void izquierdaBR(){
  regresarBI();
  delay(400);
  detener(brazoI2,brazoI1);
}
void moverBD(){
  digitalWrite(brazoD1,LOW);
  digitalWrite(brazoD2,HIGH);
}
void regresarBD(){
  digitalWrite(brazoD1,HIGH);
  digitalWrite(brazoD2,LOW);
  
}
void detener(int n1, int n2){
  digitalWrite(n1,LOW);
  digitalWrite(n2,LOW);
}

void moverBI(){
  digitalWrite(brazoI1,HIGH);
  digitalWrite(brazoI2,LOW);
}
void regresarBI(){
  digitalWrite(brazoI1,LOW);
  digitalWrite(brazoI2,HIGH);
}

void adelante(){
 for(int i=0;i<3;i++){
  digitalWrite(ruedaI1,HIGH);
  digitalWrite(ruedaI2,LOW);
  digitalWrite(ruedaD1,HIGH);
  digitalWrite(ruedaD2,LOW);
  delay(1000);
  detener();
  if(sensor()==true) break;
 }
    
}
void avanza(){
  adelante();
}


void atras(){
  for(int i=0;i<3;i++){
    digitalWrite(ruedaI1,LOW);
    digitalWrite(ruedaI2,HIGH);
    digitalWrite(ruedaD1,LOW);
    digitalWrite(ruedaD2,HIGH);
    delay(600);
    detener();
    if(sensor()==true) break;
  }
}

void detener(){
  digitalWrite(ruedaI1,LOW);
  digitalWrite(ruedaI2,LOW);
  digitalWrite(ruedaD1,LOW);
  digitalWrite(ruedaD2,LOW);
}
void giro_derechaP(){
  digitalWrite(ruedaI1,HIGH);
  digitalWrite(ruedaI2,LOW);
  digitalWrite(ruedaD1,LOW);
  digitalWrite(ruedaD2,LOW);
  delay(50);
  detener(); 
}
void giro_izquierdaP(){
  digitalWrite(ruedaI1,LOW);
  digitalWrite(ruedaI2,LOW);
  digitalWrite(ruedaD1,HIGH);
  digitalWrite(ruedaD2,LOW);
  delay(50);
  detener(); 
}

void giro_derecha(){
  for(int i=0;i<3;i++){
    digitalWrite(ruedaI1,HIGH);
    digitalWrite(ruedaI2,LOW);
    digitalWrite(ruedaD1,LOW);
    digitalWrite(ruedaD2,LOW);
    delay(333);
    detener(); 
    if(sensor()==true) break;
  }
}
void giro_izquierda(){
  for(int i=0;i<3;i++){
    digitalWrite(ruedaI1,LOW);
    digitalWrite(ruedaI2,LOW);
    digitalWrite(ruedaD1,HIGH);
    digitalWrite(ruedaD2,LOW);
    delay(333);
    detener(); 
    if(sensor()==true) break;
  }
}
void luz_on(){
  digitalWrite(luz,HIGH);
}
void luz_off(){
  digitalWrite(luz,LOW);
}

void pensar(){
  for(int i=0;i<2;i++){
    digitalWrite(ruedaI1,HIGH);
    digitalWrite(ruedaI2,LOW);
    digitalWrite(ruedaD1,LOW);
    digitalWrite(ruedaD2,LOW);
    delay(130);
    detener(); 
     digitalWrite(ruedaI1,LOW);
    digitalWrite(ruedaI2,LOW);
    digitalWrite(ruedaD1,HIGH);
    digitalWrite(ruedaD2,LOW);
    delay(130);
    detener(); 
     digitalWrite(ruedaI1,LOW);
    digitalWrite(ruedaI2,HIGH);
    digitalWrite(ruedaD1,LOW);
    digitalWrite(ruedaD2,LOW);
    delay(130);
    detener(); 
    digitalWrite(ruedaI1,LOW);
    digitalWrite(ruedaI2,LOW);
    digitalWrite(ruedaD1,LOW);
    digitalWrite(ruedaD2,HIGH);
    delay(130);
    detener(); 
    if(sensor()==true) break;
    parpadeo();
  }
}

void aqui(){
  for(int i=0;i<2;i++){
    digitalWrite(ruedaI1,HIGH);
    digitalWrite(ruedaI2,LOW);
    digitalWrite(ruedaD1,LOW);
    digitalWrite(ruedaD2,LOW);
    delay(130);
    detener(); 
     digitalWrite(ruedaI1,LOW);
    digitalWrite(ruedaI2,LOW);
    digitalWrite(ruedaD1,HIGH);
    digitalWrite(ruedaD2,LOW);
    delay(130);
    detener(); 
     digitalWrite(ruedaI1,LOW);
    digitalWrite(ruedaI2,HIGH);
    digitalWrite(ruedaD1,LOW);
    digitalWrite(ruedaD2,LOW);
    delay(130);
    detener(); 
    digitalWrite(ruedaI1,LOW);
    digitalWrite(ruedaI2,LOW);
    digitalWrite(ruedaD1,LOW);
    digitalWrite(ruedaD2,HIGH);
    delay(130);
    detener();
    if(sensor()==true) break;
    parpadeo();
  }
}

void derecha(){
  giro_derecha();
  delay(100);
  if(sensor()==false)
  adelante();
}
void izquierda(){
  giro_izquierda();
  delay(100);
  if(sensor()==false)
  adelante();
}
void giro_derecha_total(){
  for(int i=0;i<3;i++){
    digitalWrite(ruedaI1,HIGH);
    digitalWrite(ruedaI2,LOW);
    digitalWrite(ruedaD1,LOW);
    digitalWrite(ruedaD2,LOW);
    delay(1000);
    detener(); 
    if(sensor()==true) break;
  }
}
void giro_izquierda_total(){
  for(int i=0;i<3;i++){
    digitalWrite(ruedaI1,LOW);
    digitalWrite(ruedaI2,LOW);
    digitalWrite(ruedaD1,HIGH);
    digitalWrite(ruedaD2,LOW);
    delay(1000);
    detener(); 
    if(sensor()==true) break;
  }
}

void parpadeo(){
  for(int i=0;i<3;i++){
    sensor();
    luz_on();
    delay(300);
    luz_off();
    delay(300);
  }
}
