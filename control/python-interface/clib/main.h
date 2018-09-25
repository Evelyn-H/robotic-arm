int serial_init(char* port, int baud);

void command_reset(void);
void command_set(int servo, float a);
void command_set_all(float a0, float a1, float a2, float a3);
void command_move_to(float a0, float a1, float a2, float a3, int duration);

int main(void);
