%LetterStatisticsDemo

clear all
close all

wordsPerLine = 15;
allowedChar = 'abcdefghijklmnopqrstuvwxyz ''';

%%
    %N = 1

    counts = letterStatistics('gatsby.txt',allowedChar,1);
    res = PermsRep(allowedChar,1);

    %Bar Graph
    label = cellstr(res);
    bar(counts);
    set(gca,'XTick',1:length(res));
    set(gca,'XTickLabel',label);
   
    allowedChar;
    strLength = 1000;
    simulatedString = simulateIndep(allowedChar, counts, strLength);

    %Print to Outfile
    writeString('Outfile.txt',simulatedString,wordsPerLine);
    
%%
    %N = 2
    
    counts = letterStatistics('gatsby.txt',allowedChar,2);
    res = PermsRep(allowedChar,2);
   
    %RESHAPE 
    MM = reshape(counts,[],length(allowedChar));
    
    for i = 1:28
        rowsum = sum(MM(i, :));
        MM(i, :) = MM(i, :)*1/rowsum;    
    end 
    
    label = res;
    ylabel = label(:,2);
    ylabel = ylabel(1:length(allowedChar));
    xlabel = label(:,2);
    xlabel = xlabel(1:length(allowedChar));
    
    imagesc(MM);
    colormap(gray);
    set(gca,'XAxisLocation','top');
    set(gca,'XTick',1:length(allowedChar));
    set(gca,'XTickLabel',xlabel);
    
    set(gca,'YTick',1:length(allowedChar));
    set(gca,'YTickLabel',ylabel);
    
    strLength = 1000;
    simulatedString = simulateMarkov(allowedChar, counts, 2, strLength);    
    
    
    %Print to Outfile
    writeString('Outfile.txt',simulatedString,wordsPerLine);
    
%%
    %N = 3
    
    counts = letterStatistics('gatsby.txt',allowedChar,3);
    
    strLength = 1000;
    simulatedString = simulateMarkov(allowedChar, counts, 3, strLength);

    %Print to Outfile
    writeString('Outfile.txt',simulatedString,wordsPerLine);

%%
    %N = 4

    counts = letterStatistics('gatsby.txt',allowedChar,4);
    
    strLength = 1000;
    simulatedString = simulateMarkov(allowedChar, counts, 4, strLength);

    %Print to Outfile
    writeString('Outfile.txt',simulatedString,wordsPerLine);
    
    