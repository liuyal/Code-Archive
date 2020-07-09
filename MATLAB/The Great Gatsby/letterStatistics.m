function counts = letterStatistics(filename, allowedChar,N)

if  N < 1 || nargin < 3
    N = 1;
end

%Input
file = fopen(filename,'rt');
scanline = fscanf(file,'%c');

%Format
text = lower(scanline);
text = regexprep(text,'[^abcdefghijklmnopqrstuvwxyz'' ]','');
text = regexprep(text,'\n',' ');
text = regexprep(text,'-',' ');
text = regexprep(text,'  ',' ');

str_text = mat2str(text);
A = str_text;

combo = PermsRep(allowedChar,N);

TempCell = {0};
counts = 0;

%Detect Freq of combo
for ii = 1:length(combo)
    
    B = combo(ii,:);
    TempCell{ii} = strfind(A,B);

end

%Put into array counts
for iii = 1:length(combo)
    
    freq = TempCell{iii};
    
    if freq == 0 

    counts(iii) = 0;
    else
    counts(iii)= length(freq);
    
    end
    
end


fclose(file);

end
