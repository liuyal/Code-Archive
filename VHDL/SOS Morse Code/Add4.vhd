Library ieee;
Use ieee.std_logic_1164.all;
Use ieee.numeric_std.all;

Entity Add4 is
	Port (
			input1, input2 : in signed (3 downto 0);
			Carry : out signed;
			output : out signed (3 downto 0)
	);
	
End Entity Add4;


Architecture COND of Add4 is


Begin

	output <= input1 + input2;


END COND;