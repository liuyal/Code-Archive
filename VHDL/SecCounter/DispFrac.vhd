LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY DispFrac IS
PORT (
	X : in std_LOGIC_vector  (5 downto 0);
	TenX : out std_LOGIC_vector  (9 downto 0)
);
END ENTITY DispFrac;

ARCHITECTURE Behaviour OF DispFrac IS
	
	Signal A : unsigned (9 downto 0);
	

	
BEGIN
	
	A <= ('0' & unsigned(X) & "000") + ("000" & unsigned(X) & '0');
	
	TenX <= std_LOGIC_vector(A);
	
	
	--TenX(0) <= '0';
	--TenX(1) <= X(0);
	--TenX(2) <= X(1);
	--obj0 : work.FullAdder Port Map( A=>X(0) , B =>X(2), C =>'0', Sum => TenX(3), Carry => wireA);
   --obj1 : work.FullAdder Port Map( A=>X(1) , B =>X(3), C =>wireA, Sum => TenX(4), Carry => wireB);
  	--obj2 : work.FullAdder Port Map( A=>X(2) , B =>X(4), C =>wireB, Sum => TenX(5), Carry => wireC);
	--obj3 : work.FullAdder Port Map( A=>X(3) , B =>X(5), C =>wireC, Sum => TenX(6), Carry => wireD);
	--obj4 : work.HalfAdder Port Map( A=>X(4) , B =>wireD, Sum => TenX(7), Carry => wireE);
	--obj5 : work.HalfAdder Port Map( A=>X(5) , B =>wireE, Sum => TenX(8), Carry => TenX(9));

END Behaviour;








