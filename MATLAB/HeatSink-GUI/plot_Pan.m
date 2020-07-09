% *********************** Main Plot Function ***********************
function y = plot_Pan(hObject, eventdata, handles)
% Reset Plot for each new input
delete(handles.axes1.Children);
% No Runs Selected
M = handles.panel;
if sum(M) == 0 || isempty(handles.plot_data)
    plot(0);
    grid minor
    xlim([0 4]);
    ax = gca;
    ax.XTick = [1 2 3];
    ax.XTickLabel = 'X';
    ax.YLabel.String = ['Temperature ' char(176) 'C'];
    return
end
% Control of PLot Type (Thermal R)
if handles.plot_option.PlotMode == 3;
    plot_TR(hObject, eventdata, handles,M);
    return;
end
%Load Names/Runs/Labels
for i = 1:length(handles.plot_data)
    names{i} = handles.plot_data{i}.FolderName;
end
Runs = {'R1','R2','R3','R4','R5','R6','R7'};
Vec = handles.panel;
Vec = ~Vec;
Runs(Vec) = [];

% Load data
hold on
for j = 1:length(handles.plot_data)
    pdata = handles.plot_data{j}.Data;
    savedata{j} = pdata;
    % Load Index of 3 lables
    labels2 = handles.plot_data{j}.Header;
    index1 = find(strcmp(labels2, 'Diode Internal'));
    index2 = find(strcmp(labels2, 'HS Bottom'));
    if isempty(index2)
        index2 = find(strcmp(labels2, 'Heat Sink'));
    end
    index3 = find(strcmp(labels2, 'Ambient In'));
    labels2 = labels2([index1 index2 index3]);
    % Load Data
    for i = 1:size(pdata,1);
        y(i,:) = pdata(i,[index1 index2 index3]);
    end
    % Load Error
    for i = 1:size(pdata,1);
        err(i,:) = pdata(i,[index1+1 index2+1 index3+1]);
    end
    err(isnan(err)) = 0;
    
    % ***********************  Calc Ambient 0 ***********************
    if handles.plot_option.PlotMode == 2;
        for ii = 1:length(y)
            amb = y(ii,end);
            y(ii,:) = y(ii,:) - amb;
        end
    end % *********************** End Calc Ambient 0 ***********************
    
    % Plot Data - Color - Marker
    indx = find(M);
    y = y(indx,:).';
    err = err(indx,:).';
    err = sqrt(err.^2+1);
    for o = 1:length(Runs)
        if handles.plot_option.ErrorBars == 1
            P = errorbar(y(:,o),err(:,o),styles(o),'LineWidth',2,'color',color_index(j));
        else
            P = plot(y(:,o),styles(o),'LineWidth',2,'color',color_index(j));
        end
    end
    clear y err
end
hold off

% Plot Misc Settings
if ~isempty(names) % Legend Names Edit
    co = [];
    for i = 1:length(names)
        m = repmat(names(i),length(Runs),1);
        co = [co;m Runs'];
    end
end
m = strcat(co(:,1),{' - '}, co(:,2));
legend('-DynamicLegend',m);

% Slope Uncertainity Fillers ***************************************
if handles.plot_option.SlopeUn == 1
    hold on
    for j = 1:length(handles.plot_data)
        pdata = handles.plot_data{j}.Data;
        
        savedata{j} = pdata;
        % Load Index of 3 lables
        labels2 = handles.plot_data{j}.Header;
        index1 = find(strcmp(labels2, 'Diode Internal'));
        index2 = find(strcmp(labels2, 'HS Bottom'));
        index3 = find(strcmp(labels2, 'Ambient In'));
        labels2 = labels2([index1 index2 index3]);
        % Load Data
        for i = 1:size(pdata,1);
            y(i,:) = pdata(i,[index1 index2 index3]);
        end
        % Load Error
        for i = 1:size(pdata,1);
            err(i,:) = pdata(i,[index1+1 index2+1 index3+1]);
        end
        err(isnan(err)) = 0;
        
        % ***********************  Calc Ambient 0 ***********************
        if handles.plot_option.PlotMode == 2;
            for ii = 1:length(y)
                amb = y(ii,end);
                y(ii,:) = y(ii,:) - amb;
            end
        end % *********************** End Calc Ambient 0 ***********************
        
        % Plot Data - Color - Marker
        indx = find(M);
        y = y(indx,:).';
        err = err(indx,:).';
        err = sqrt(err.^2+1);
        for o = 1:length(Runs)
            unslopefiller(y(:,o),err(:,o),color_index(j),o,j,1);
        end
        clear y err
    end
    hold off
end
% ************************************************
grid on

xlim([1 3]);
ylim([handles.plot_option.MinPlot handles.plot_option.MaxPlot])
yspace = handles.plot_option.MinPlot : handles.plot_option.PlotTick : handles.plot_option.MaxPlot;
set(handles.axes1, 'YTick', yspace);
set(handles.axes1, 'YTickLabel', num2cell(yspace'));
ax = gca;
ax.XTick = [1 2 3];
ax.XTickLabel = labels2;
ax.YLabel.String = ['Temperature ' '[' char(176) 'C]'];
end

% ***********************  Plot Thermal R ***********************
function P = plot_TR(hObject, eventdata, handles,M)
%Load Names/Runs/Labels
for i = 1:length(handles.plot_data)
    names{i} = handles.plot_data{i}.FolderName;
end
Runs = {'R1','R2','R3','R4','R5','R6','R7'};
Vec = handles.panel;
Vec = ~Vec;
Runs(Vec) = [];
Mat = zeros(length(find(M)),length(names),2);

%Load Data
for j = 1:length(handles.plot_data)
    pdata = handles.plot_data{j}.Data;
    %Find Index for labels
    labels2 = handles.plot_data{j}.Header;
    index1 = find(strcmp(labels2, 'U (DMM)'));
    index2 = find(strcmp(labels2, 'I'));
    if isempty(index2)
        index2 = find(strcmp(labels2, 'Diode I'));
    end
    index2 = index2(1);
    index3 = find(strcmp(labels2, 'Diode Internal'));
    if isempty(index3)
        index3 = find(strcmp(labels2, 'Diode (+)'));
    end
    index4 = find(strcmp(labels2, 'HS Bottom'));
    if isempty(index4)
        index4 = find(strcmp(labels2, 'Heat Sink'));
    end
    index5 = find(strcmp(labels2, 'Ambient In'));
    %Load value from struc
    for i = 1:size(pdata,1);
        y(i,:) = pdata(i,[index1 index2 index3 index4 index5]);
    end
    R = (y(:,3)-y(:,5))./(y(:,1).*y(:,2));
    TCR = (y(:,3)-y(:,4))./(y(:,1).*y(:,2));
    Rest = (y(:,4)-y(:,5))./(y(:,1).*y(:,2));
    indx = find(M);
    Z = R(indx,:);
    ZTCR = TCR(indx,:);
    ZRest = Rest(indx,:);
    
    Mat(:,j,1) = ZTCR;
    Mat(:,j,2) = ZRest;
    
    clear y R TCR Rest Z ZTCR ZRest
end
colormap lines

if length(find(M))== 1 && length(names) == 1
    %single RUn ADD
    xP = [Mat(:,:,1) Mat(:,:,2); 0 0];
    bar(xP,0.5,'stack');
    xlim([0 2]);
    for i = 1:length(handles.axes1.Children)
        if mod(i,2) ~= 0
            handles.axes1.Children(i).FaceColor = [0.8500 0.3250 0.0980];
        end
    end
elseif length(find(M))== 1 && length(names) > 1
    xP = Mat(:,:,1);
    yP = Mat(:,:,2);
    zP = [xP' yP'];
    bar(zP,0.5,'stack');
    for i = 1:length(handles.axes1.Children)
        if mod(i,2) ~= 0
            handles.axes1.Children(i).FaceColor = [0.8500 0.3250 0.0980];
        end
    end
elseif length(find(M))> 1
    stackData = Mat;
    groupLabels = Runs;
    NumGroupsPerAxis = size(stackData, 1);
    NumStacksPerGroup = size(stackData, 2);
    groupBins = 1:NumGroupsPerAxis; % Count off the number of bins
    MaxGroupWidth = 0.65;           % Fraction of 1. If 1, then all bars in groups touching
    groupOffset = MaxGroupWidth/NumStacksPerGroup;
    hold on
    for i = 1:NumStacksPerGroup
        Y = squeeze(stackData(:,i,:));
        % Center the bars:
        internalPosCount = i - ((NumStacksPerGroup+1) / 2);
        % Offset the group draw positions:
        groupDrawPos = (internalPosCount)* groupOffset + groupBins;
        h(i,:) = bar(Y, 'stacked');
        set(h(i,:),'BarWidth',groupOffset);
        set(h(i,:),'XData',groupDrawPos);
    end
    hold off
    set(gca,'XTickMode','manual');
    set(gca,'XTick',1:NumGroupsPerAxis);
    set(gca,'XTickLabelMode','manual');
    set(gca,'XTickLabel',groupLabels);
    xlim([0 length(find(M))+1]);
    
    for i = 1:length(handles.axes1.Children)
        if mod(i,2) ~= 0
            handles.axes1.Children(i).FaceColor = [0.8500 0.3250 0.0980];
        end
    end
end

legend({'TCR','Rest'});

grid on
ylim([handles.plot_option.MinPlot handles.plot_option.MaxPlot])
yspace = handles.plot_option.MinPlot : handles.plot_option.PlotTick : handles.plot_option.MaxPlot;
set(handles.axes1, 'YTick', yspace);
set(handles.axes1, 'YTickLabel', num2cell(yspace'));
ax = gca;
ax.XTickLabel = Runs;
ax.YLabel.String = ['Thermal Resistance ' '[' char(176) 'C/W]'];
grid minor
end

% *********************** Helper Functions ***********************
function colors = color_index(j)

if j == 1
    colors = [1 0 0]; % Red
elseif j == 2
    colors = [1 0.5 0]; % Orange
elseif j == 3
    colors = [0/255 153/255 0/255]; % Gold
elseif j == 4
    colors = [0 1 0]; % Green
elseif j == 5
    colors = [0 1 1]; % Cyan
elseif j == 6
    colors = [0 0.5 1]; % Blue
elseif j == 7
    colors = [0.5 0 1]; % Purple
elseif j == 8
    colors = [1 0 0.5]; % Pink
elseif j == 9
    colors = [0 0.5 0.5]; % Teal
elseif j == 10
    colors = [0.5 0 0]; % Maroon
elseif j == 11
    colors = [0 0 0]; % Black
else
    colors = [1 1 1]; %White
end

end

function styles = styles(o)

if o == 1
    styles = '-';
elseif o == 2
    styles =  '--';
elseif o == 3
    styles =  ':';
elseif o == 4
    styles =  '-.';
elseif o == 5
    styles =  ':x';
elseif o == 6
    styles =  '--+';
elseif o == 7
    styles =  '-.*';
end

end

function unslopefiller(y,err,color,o,j,EB)

top = [y(1)+err(1), y(2)-err(2), y(3)+err(3)];
bottom = [y(1)-err(1), y(2)+err(2), y(3)-err(3)];
A = top(1);
B = bottom(1);
C = top(2);
D = bottom(2);
E = top(3);
F = bottom(3);
M1 = (top(1)+top(2))/2;
M2 = (bottom(2)+bottom(3))/2;
xpoints = [1 1 1.5; 1.5 2 2; 2 2 2.5; 2.5 3 3];
ypoints = [A B M1; M1 C D; C D M2; M2 E F];

for i = 1:length(xpoints)
    pat = patch(xpoints(i,:),ypoints(i,:),color);
    pat.FaceAlpha = 0.5;
    pat.EdgeColor = color;
    pat.EdgeAlpha = 0.25;
end
clear top bottom A B C D E F M1 M2 xpoints ypoints
end


