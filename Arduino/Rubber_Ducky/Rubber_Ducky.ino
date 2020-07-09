/**
 * Made with Duckuino, an open-source project.
 * Check the license at 'https://github.com/Dukweeno/Duckuino/blob/master/LICENSE'
 */

#include "Keyboard.h"

void typeKey(uint8_t key)
{
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}

/* Init function */
void setup()
{
  // Begining the Keyboard stream
  Keyboard.begin();

  // Wait 500ms
  delay(500);

  delay(3000);
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  Keyboard.releaseAll();

  delay(500);
  Keyboard.print(F("notepad"));

  delay(500);
  typeKey(KEY_RETURN);

  delay(750);
  typeKey(KEY_RETURN);

  Keyboard.print(F("                               .___."));

  typeKey(KEY_RETURN);

  Keyboard.print(F("           /)               ,-^     ^-."));

  typeKey(KEY_RETURN);

  Keyboard.print(F("          //               /           \\"));

  typeKey(KEY_RETURN);

  Keyboard.print(F(" .-------| |--------------/  __     __  \\-------------------.__"));

  typeKey(KEY_RETURN);

  Keyboard.print(F(" |WMWMWMW| |>>>>>>>>>>>>> | />>\\   />>\\ |>>>>>>>>>>>>>>>>>>>>>>:>"));

  typeKey(KEY_RETURN);

  Keyboard.print(F(" `-------| |--------------| \\__/   \\__/ |-------------------'^^"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("          \\\\               \\    /|\\    /"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("           \\)               \\   \\_/   /"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("                             |       |"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("                             |+H+H+H+|"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("                             \\       /"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("                              ^-----^"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("               +------------------------------------+"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("               | >>> IHR COMPUTER WURDE GEHACKT <<< |"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("               +------------------------------------+"));

  typeKey(KEY_RETURN);

  typeKey(KEY_RETURN);

  Keyboard.print(F("                Alle Ihre Passwoerter wurden mir"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("                inklusive Ihrer EBanking-Zugangsdaten"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("                ueber das Internet uebermittelt..."));

  typeKey(KEY_RETURN);

  typeKey(KEY_RETURN);

  Keyboard.print(F("                Vielen Dank fuer Ihre Unterstuetzung!"));

  typeKey(KEY_RETURN);

  typeKey(KEY_RETURN);

  Keyboard.print(F("               ======================================="));

  typeKey(KEY_RETURN);

  Keyboard.print(F("               +++ HACKING +++ HACKING +++ HACKING +++"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("               ======================================="));

  typeKey(KEY_RETURN);

  // Ending stream
  Keyboard.end();
}

/* Unused endless loop */
void loop() {}
