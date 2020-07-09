function writeString(filename,str,wordsPerLine)

if wordsPerLine < 1 || nargin < 3
    wordsPerLine = 15;
end

%Input
file = fopen(filename,'wt');
str = strsplit(str);

%Number of Lines
index = floor(length(str)/wordsPerLine);
AcIndex = (length(str)/wordsPerLine);

%Detect lastline and iso
lastlinestr = str;

if AcIndex > index
for i = 1:(index*wordsPerLine)
    lastlinestr {i} = {};
end
    lastline = lastlinestr;
    lastline(cellfun('isempty',lastline)) = [];
    lastline = strjoin(lastline,' ');
else
    lastline = {};
end

%Format into words per line
A = 1;
Newstr = {0};
for ii = 1:index
   B = ii*wordsPerLine;
   Newstr{ii} = sprintf('%s ',str{(A:B)});
   A = 1 + B;  
end

%Add last line if any
if AcIndex > index
    Newstr{ii+1} = lastline;
else
    %add nothing
end

%Print
Wr = strjoin(Newstr,'\n');
fprintf(file,'%s \n \n',Wr);

fclose(file);

end