#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <signal.h>
#include <assert.h>

#define COMMAND_LENGTH 1024
#define NUM_TOKENS (COMMAND_LENGTH / 2 + 1)

#define HISTORY_DEPTH 10
char history[HISTORY_DEPTH][COMMAND_LENGTH];
int history_Counter = 0;
static volatile int keepRunning = 1;

/* Save history only keep last 10 commands*/
void history_command(char *tokens[], int length, int token_count, _Bool *in_background)
{
	if(tokens[0] == NULL) {return;}
	
	if (*in_background) { token_count--;}
	
	int D = 0;
	int k = 0;

	if (history_Counter >= 10)
	{
		for (int k = 0; k < HISTORY_DEPTH - 1; k++)
		{
			strcpy(history[k],history[k+1]);
		}

		k = 9;
	}
	else
	{
		k = history_Counter;
	}

	for (int j = 0; j < token_count; j++)
	{
		for (int i = 0; i < length-1; i++)
		{
			if (tokens[j][i] == '\0')
			{
				history[k][D] = ' ';
			}
			else
			{
				history[k][D] = tokens[j][i];
			}
			D++;
		}
	}

	for (int u = length-1; u < COMMAND_LENGTH; u++){history[k][u] = '\0';}

	history_Counter++;
}

/*Print history of last 10 commands*/
void print_history()
{
	if (history_Counter == 0) {return;}

	int i = 0;
	int k = 0;
 	char snum[10];

	if (history_Counter < HISTORY_DEPTH+1)
	{
		for (i = 0; i < history_Counter; i++)
		{	
			sprintf(snum, "%d\t", i+1);
			write(STDOUT_FILENO, snum, strlen(snum));
			write(STDOUT_FILENO, history[i], strlen(history[i]));
			write(STDOUT_FILENO, "\n", strlen("\n"));
		}
	}
	else
	{
		k = history_Counter - 9;

		for (i = k; i < history_Counter + 1; i++)
		{
			sprintf(snum, "%d\t", i);
			write(STDOUT_FILENO, snum, strlen(snum));
			write(STDOUT_FILENO, history[i-k], strlen(history[i-k]));
			write(STDOUT_FILENO, "\n", strlen("\n"));
		}
	}
}

/* To handel internal commands */
bool internal_command(char *tokens[])
{	
	if (tokens[0] == NULL) { return true; }

	if (strcmp(tokens[0], "exit") == 0)
	{
		write(STDOUT_FILENO, "cmd exit\n", strlen("cmd exit\n"));
		exit(0);
	}
	else if (strcmp(tokens[0], "pwd") == 0)
	{
		char cwd_buff[COMMAND_LENGTH];
		getcwd(cwd_buff, sizeof(cwd_buff));

		if (cwd_buff != NULL)
		{
			write(STDOUT_FILENO, cwd_buff, strlen(cwd_buff));
			write(STDOUT_FILENO, "\n", strlen("\n"));
		}
		else
		{
			perror("Error getting cwd.");
		}

		return true;
	}
	else if  ((strcmp(tokens[0], "cd") == 0))
	{
		if(chdir(tokens[1]) != 0)
		{
			write(STDOUT_FILENO, "Invalid directory.\n", strlen("Invalid directory.\n"));
		}
		return true;
	}
	else if (strcmp(tokens[0], "history") == 0)
	{
		print_history();
		return true;
	}
	else if(strcmp(tokens[0], "!!") == 0)
	{
		return true;
	}
	else if (tokens[0][0] == '!')
	{
		return true;
	}

	return false;
}

/*Command Input and Processing

 * Tokenize the string in 'buff' into 'tokens'.
 * buff: 	Character array containing string to tokenize.
 *       	Will be modified: all whitespace replaced with '\0'
 * tokens:  array of pointers of size at least COMMAND_LENGTH/2 + 1.
 *       	Will be modified so tokens[i] points to the i'th token
 *      	in the string buff. All returned tokens will be non-empty.
 *      	NOTE:in_background pointers in tokens[] will all point into buff!
 *       	Ends with a null pointer.
 * returns: number of tokens.
 */
int tokenize_command(char *buff, char *tokens[])
{
	int token_count = 0;
	_Bool in_token = false;
	int num_chars = strnlen(buff, COMMAND_LENGTH);
	for (int i = 0; i < num_chars; i++) {
		switch (buff[i]) {
			// Handle token delimiters (ends):
		case ' ':
		case '\t':
		case '\n':
			buff[i] = '\0';
			in_token = false;
			break;

			// Handle other characters (may be start)
		default:
			if (!in_token) {
				tokens[token_count] = &buff[i];
				token_count++;
				in_token = true;
			}
		}
	}
	tokens[token_count] = NULL;
	return token_count;
}

/**
 * Read a command from the keyboard into the buffer 'buff' and tokenize it
 * such that 'tokens[i]' points into 'buff' to the i'th token in the command.
 * buff: Buffer allocated by the calling code. Must be at least
 *       COMMAND_LENGTH bytes long.
 * tokens[]: Array of character pointers which point into 'buff'. Must be at
 *       	 least NUM_TOKENS long. Will strip out up to one final '&' token.
 *       	 tokens will be NULL terminated (a NULL pointer indicates end of tokens).
 * in_background: pointer to a boolean variable. Set to true if user entered
 *       an & as their last token; otherwise set to false.
 */
void read_command(char *buff, char *tokens[], _Bool *in_background)
{	
	*in_background = false;

	// Read input
	int length = read(STDIN_FILENO, buff, COMMAND_LENGTH - 1);

	if (length < 0 && (errno != EINTR)) {
		perror("Unable to read command from keyboard. Terminating.\n");
		exit(-1);
	}

	// Null terminate and strip \n.
	buff[length] = '\0';
	if (buff[strlen(buff) - 1] == '\n') {
		buff[strlen(buff) - 1] = '\0';
	}


	// Tokenize (saving original command string)
	int token_count = tokenize_command(buff, tokens);
	if (token_count == 0) {
		return;
	}

	// Extract if running in background:
	if (token_count > 0 && strcmp(tokens[token_count - 1], "&") == 0) {
		*in_background = true;
		tokens[token_count - 1] = 0;
	}

	if (strcmp(buff, "!!") == 0)
	{
		if (history_Counter == 0)
		{
			write(STDOUT_FILENO, "SHELL: Unknown history command.\n", strlen("SHELL: Unknown history command.\n"));
			return;
		}

		int index = 0;

		if (history_Counter < HISTORY_DEPTH)
		{
			index = history_Counter - 1;
			write(STDOUT_FILENO, history[index], strlen(history[index]) );
			write(STDOUT_FILENO, "\n", strlen("\n"));
			strcpy(buff,history[index]);
		}
		else
		{
			index = 9;
			write(STDOUT_FILENO, history[index], strlen(history[index]) );
			write(STDOUT_FILENO, "\n", strlen("\n"));
			strcpy(buff,history[index]);
		}
		length = strlen(buff)+1;
		token_count = tokenize_command(buff, tokens);
		if (token_count == 0) {return;}
	}
	else if (tokens[0][0] == '!')
	{
		if (history_Counter == 0)
		{
			write(STDOUT_FILENO, "SHELL: Unknown history command.\n", strlen("SHELL: Unknown history command.\n"));
			return;
		}

		char *value = tokens[0] + 1;
		int index = atoi(value);

		if (index <= 0)
		{
			write(STDOUT_FILENO, "SHELL: Unknown history command.\n", strlen("SHELL: Unknown history command.\n"));
			return;
		}
		
		if (history_Counter < HISTORY_DEPTH)
		{
			index = index - 1;
			write(STDOUT_FILENO, history[index], strlen(history[index]) );
			write(STDOUT_FILENO, "\n", strlen("\n"));
			strcpy(buff,history[index]);
		}
		else
		{
			int low = history_Counter - 9;
			int high = history_Counter;

			if (index < low || index > high)
			{
				write(STDOUT_FILENO, "Error: History Out of Range\n", strlen("Error: History Out of Range\n"));
				return;
			}

			index = index - low;
			write(STDOUT_FILENO, history[index], strlen(history[index]) );
			write(STDOUT_FILENO, "\n", strlen("\n"));
			strcpy(buff,history[index]);
		}


		length = strlen(buff)+1;
		token_count = tokenize_command(buff, tokens);
		if (token_count == 0) {return;}

	}

	if (keepRunning == 0){tokens[0] = ""; return; }
	
	history_command(tokens, length, token_count,in_background);
}

/* Signal handler function */
void handle_SIGINT()
{
	write(STDOUT_FILENO, "\n", strlen("\n"));
	keepRunning = 0;
	print_history();
  	signal(SIGINT, handle_SIGINT);
}

/* Main and Execute Commands*/
int main(int argc, char* argv[])
{
	char input_buffer[COMMAND_LENGTH];
	char *tokens[NUM_TOKENS];

	  /* Set up the signal handler */
  	struct sigaction handler;
  	handler.sa_handler = handle_SIGINT;
  	handler.sa_flags = 0;
  	sigemptyset(&handler.sa_mask);
  	sigaction(SIGINT, &handler, NULL);

  	if(signal(SIGINT, handle_SIGINT) == SIG_ERR)
  	{
    	write(STDOUT_FILENO, "SIGINT Error\n", strlen("SIGINT Error\n"));
  	}


	while (true) {

		// Display current work directory in shell
		char cwd_buff[COMMAND_LENGTH];
		getcwd(cwd_buff, sizeof(cwd_buff));
		write(STDOUT_FILENO, cwd_buff, strlen(cwd_buff));

		// Get command
		// Use write because we need to use read() to work with
		// signals, and read() is incompatible with printf().
		write(STDOUT_FILENO, "> ", strlen("> "));
		_Bool in_background = false;
		read_command(input_buffer, tokens, &in_background);

		/*for (int i = 0; tokens[i] != NULL; i++) {
			write(STDOUT_FILENO, "   Token: ", strlen("   Token: "));
			write(STDOUT_FILENO, tokens[i], strlen(tokens[i]));
			write(STDOUT_FILENO, "\n", strlen("\n"));
		}
		if (in_background) {
			write(STDOUT_FILENO, "Run in background.", strlen("Run in background."));
		}*/

		bool is_interal = internal_command(tokens);

		/** Steps For Basic Shell:
		 * 1. Fork a child process
		 * 2. Child process invokes execvp() using results in token array.
		 * 3. If in_background is false, parent waits for
		 *    child to finish. Otherwise, parent loops back to
		 *    read_command() again immediately.*/

		if (keepRunning == 1 && !is_interal)
		{
			pid_t child_pid;
			int status;

			child_pid = fork();

			if (child_pid == 0) // Child process
			{
				if (execvp(tokens[0], tokens) == -1)
				{
					char *msg = tokens[0];
					char *msg2 = ": Unknown command\n";

					write(STDOUT_FILENO, msg, strlen(msg));
					write(STDOUT_FILENO, msg2, strlen(msg2));
					exit(EXIT_FAILURE);
				}

				exit(EXIT_SUCCESS);
			}
			else if (child_pid > 0) // Parebt process
			{
				if (!in_background)
				{
					if (waitpid(child_pid, &status, 0) == -1)
					{
						exit(EXIT_FAILURE);
					}
				}
			}

			// Cleaup zombie processes
			while (waitpid(-1, NULL, WNOHANG) > 0) { ; }
		}
		else
		{
			keepRunning = 1;
		}
	} // makewhile (true)
	return 0;
}
