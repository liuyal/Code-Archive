Library ieee;
Use ieee.std_logic_1164.all;
Use ieee.numeric_std.all;

Entity ToneGen_Test is
	Port (
			SW : in std_logic_vector(17 downto 0);
			SamClk : in std_logic;
			KEY : in std_logic_vector(3 downto 0);
			AudioOut : out signed (15 downto 0)
	);
End Entity ToneGen_Test;


Architecture COND of ToneGen_Test is
	

Begin

	Test: Entity work.ToneGenerator port map (
			Freq => unsigned(SW (15 downto 0)), clear => KEY(1), WaveOut => AudioOut, clk => SamClk );

End COND;