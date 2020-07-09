function simulatedString = simulateIndep(allowedChar, counts, strLength)
%This function generates a string of randomly chosen symbols. The symbols
%are independent and distributed according to their frequencies in array
%"counts".
%
% INPUTS:
%   allowedChar - an array containing the symbols that can be chosen.
%   counts - the frequencies of the corresponding symbols in "allowedChar".
%   length - the number of characters in the output string.
%
% OUTPUT:
%   simulatedString - the output string of randomly chosen symbols.

%Default length is 1000 characters
if nargin < 3 || strLength < 1
    strLength = 1000;
end

%Normalize the symbol frequencies to create the probability distribution
pdf = counts/sum(counts);

%Create the cumulative distribution
cdf = [0, cumsum(pdf)];

%Monte Carlo simulation of 1st order statistics
rr = rand(1, strLength);
[~, rrLetters] = histc(rr, cdf);
simulatedString = allowedChar(rrLetters);

end

