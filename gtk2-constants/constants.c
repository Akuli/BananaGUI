#include <stdio.h>

#include <gtk/gtk.h>


void print_it(char *name, int value) {
	printf("%s = %d\n", name, value);
}


int main(void) {
	print_it("GTK_WINDOW_TOPLEVEL", GTK_WINDOW_TOPLEVEL);
/*	print_it("GTK_WINDOW_POPUP", GTK_WINDOW_POPUP);*/

	print_it("GTK_ORIENTATION_HORIZONTAL", GTK_ORIENTATION_HORIZONTAL);
	print_it("GTK_ORIENTATION_VERTICAL", GTK_ORIENTATION_VERTICAL);

/*	print_it("GTK_JUSTIFY_LEFT", GTK_JUSTIFY_LEFT);*/
/*	print_it("GTK_JUSTIFY_RIGHT", GTK_JUSTIFY_RIGHT);*/
	print_it("GTK_JUSTIFY_CENTER", GTK_JUSTIFY_CENTER);
/*	print_it("GTK_JUSTIFY_FILL", GTK_JUSTIFY_FILL);*/

	print_it("GTK_DIALOG_MODAL", GTK_DIALOG_MODAL);

	print_it("GTK_BUTTONS_NONE", GTK_BUTTONS_NONE);

	print_it("GTK_MESSAGE_INFO", GTK_MESSAGE_INFO);
	print_it("GTK_MESSAGE_WARNING", GTK_MESSAGE_WARNING);
	print_it("GTK_MESSAGE_ERROR", GTK_MESSAGE_ERROR);
	print_it("GTK_MESSAGE_QUESTION", GTK_MESSAGE_QUESTION);

	return 0;
}
