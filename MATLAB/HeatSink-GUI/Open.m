function [ArrayStruct, X] = Open(path)
% Start with a folder and get a list of all subfolders.
% that folder and all of its subfolders.
% clc; clear; close all;  % Clear the command window.
% Define a starting folder.
% Ask user to confirm or change.
% start_path = fullfile(matlabroot);
% topLevelFolder = 'C:\Users\LAEC\Desktop\GUI\Data';
topLevelFolder = path;

if topLevelFolder == 0
    return;
end

% Get list of all subfolders.
allSubFolders = genpath(topLevelFolder);
% Parse into a cell array.
remain = allSubFolders;
listOfFolderNames = {};
while true
    [singleSubFolder, remain] = strtok(remain, ';');
    if isempty(singleSubFolder)
        break;
    end
    listOfFolderNames = [listOfFolderNames singleSubFolder];
end

numberOfFolders = length(listOfFolderNames);
index = 0;
% Process all files in those folders.
for k = 1 : numberOfFolders
    %open Create data structure (inc foldername, parameter, rawdata)
    foldername = listOfFolderNames{k};
    files = dir(foldername);
    files = struct2cell(files);
    files = files(1,:);
    %Data input
    data = [];
    parameter = [];
    header = [];
    for i = 1:length(files);
        %RawDATA
        dtrue = strcmp(files{i},'Test.txt');
        if dtrue == 1;
            name = [foldername '\Test.txt'];
            fileID = fopen(name);           % open raw txt file
            rawdata = textscan(fileID,'%s', 'Delimiter',{'\r'});
            fclose(fileID);                 % close raw file
            data = rawdata{1};
            for j = 1:length(data);
                M{j} = strsplit(data{j},'\t');
            end
            data = M';
            header = data(1);
            data = data(2:end);
            for u = 1:length(data)
                temp = data{u};
                m(u,:) = temp;
            end
            for ui = 1:size(m,1)
                for uj = 1:size(m,2)
                    data{ui,uj} = str2double(m{ui,uj});
                end
            end
            data = cell2mat(data);
            index = index + 1;
            clear M m
        end
        %PARAMETER
        ptrue = strcmp(files{i},'parameters.txt');
        if ptrue == 1;
            name = [foldername '\parameters.txt'];
            fileID = fopen(name);
            txt = textscan(fileID,'%s', 'Delimiter',{'\r'});
            fclose(fileID);
            parameter = txt{1};
            for j = 1:length(parameter);
                M2{j} = strsplit(parameter{j},'\t');
            end
            parameter = M2';
            clear M2
        end
    end %Data input End
    
    %Create Structure and insert into matrix;
    Datastruct = struct('FolderName',foldername,'Header', header ,'Data',{data},'Parameter',{parameter},'Path', foldername,'Index', index);
    ArrayStruct{k} = Datastruct;
end

%Detele Top level Folders (Empty)
deletematrix = zeros(1,length(ArrayStruct));
for i = 1:length(ArrayStruct)
    temp = ArrayStruct{i};
    if isempty(temp.Data);
        deletematrix(i) = 1;
    else
        %Rename FolderName
        temp = ArrayStruct{i}.FolderName;
        ind = ismember(temp,'\');
        ind = find(ind);
        ind = ind(end);
        temp = temp(ind+1:end);
        %         ind = ismember(temp,' ');   %----Remove
        %         ind = find(ind);
        %         ind = ind(1);
        %         temp = temp(ind+1:end);     %----Numbering
        ArrayStruct{i}.FolderName = temp;
    end
end
X = [listOfFolderNames' num2cell(deletematrix') num2cell(1:length(deletematrix))'];
index = find(deletematrix);  %Delete Empty folders
ArrayStruct(index) = [];
end






