//Define pin numbers

//right motor
int m1f = 10; 
int m1r = 9;
//left motor
int m2f = 6; 
int m2r = 5;
int led = 13;
char value;
int val[3];
int len;
int direc;


void setup()
{
  //start serial communication at Baud rate of 9600
  Serial.begin(9600);
  pinMode(m1f, OUTPUT);
  pinMode(m1r, OUTPUT);
  pinMode(m2f, OUTPUT);
  pinMode(m2r, OUTPUT);
  pinMode(led, OUTPUT);
  digitalWrite(led, HIGH);
}

void execute()
{
  int no;
  int i = 0;

  //convert ASCII value from serial buffer into int
  no = value - '0';
  //Serial.println(no);

  int a, b, c, d;

  /*
    """
    Direction control Index:

    '<' , '>' are the frame check bits for serial communication

    Numbers represent the direction to be moved as per their     	position on numpad
    1: Back Left
    2: Back
    3: Back right
    4: Left
    5: Stay still
    6: Right
    7: Front Left
    8: Forward
    9: Forward right
    """
  */

  switch (no)
  {
    case 0:
      a = 0; b = 100; c = 100; d = 0;
      break;
    case 3:
      a = 0; b = 255; c = 0; d = 100;
      break;
    case 2:
      a = 0; b = 255; c = 0; d = 255;
      break;
    case 1:
      a = 0; b = 100; c = 0; d = 255;
      break;
    case 4:
      a = 255; b = 0; c = 0; d = 0;
      break;
    case 5:
      a = 0; b = 0; c = 0; d = 0;
      break;
    case 6:
      a = 0; b = 0; c = 255; d = 0;
      break;
    case 7:
      a = 255; b = 0; c = 100; d = 0;
      break;
    case 8:
      a = 150; b = 0; c = 150; d = 0;
      break;
    case 9:
      a = 100; b = 0; c = 255; d = 0;
      break;
  }
 
  analogWrite(m1f, a);
  analogWrite(m1r, b);
  analogWrite(m2f, c);
  analogWrite(m2r, d);
  //delay(255);
}

void loop()
{
  if (Serial.available())
  {
    //Check for frame control bits
    char ch = Serial.read();
    if (ch == '<')
    {
      len = 0;
    }
    else if (ch == '>')
    {
      execute();
      //Serial.println(value);
      len = 1;
    }
    else if (len == 0)
      value = ch;
  }
}
