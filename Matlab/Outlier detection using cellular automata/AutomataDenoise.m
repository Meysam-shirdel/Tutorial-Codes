%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Automata Denoising
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc
clear all

NoiseThreshold=4;
load NoiseRadius.mat;
load Automata.mat
load AutomatonIndex.mat
% NoiseRadius=500;
Dim1Size=size(AutomatonIndex,1);
Dim2Size=size(AutomatonIndex,2);

Automata=[zeros(NoiseRadius,Dim2Size);Automata;zeros(NoiseRadius,Dim2Size)];
Automata=[zeros(Dim1Size+2*NoiseRadius,NoiseRadius),Automata,zeros(Dim1Size+2*NoiseRadius,NoiseRadius)];

AutomatonIndex=[-2*ones(NoiseRadius,Dim2Size);AutomatonIndex;-2*ones(NoiseRadius,Dim2Size)];
AutomatonIndex=[-2*ones(Dim1Size+2*NoiseRadius,NoiseRadius),AutomatonIndex,-2*ones(Dim1Size+2*NoiseRadius,NoiseRadius)];

Dim1Size=size(AutomatonIndex,1);
Dim2Size=size(AutomatonIndex,2);

figure(2)
[XGrid,YGrid]=meshgrid(1:Dim2Size,1:Dim1Size);
plot(XGrid,YGrid,'.','color',[0.9 0.9 0.9]);
hold on

axis([1 Dim2Size 1 Dim1Size])
NoiseNum=0;
red=[];
green=[];
NotNoiseData=[];

for i=1+NoiseRadius:Dim1Size-NoiseRadius
    for j=1+NoiseRadius:Dim2Size-NoiseRadius
        if AutomatonIndex(i,j)~=-2  %% Is it Data?
            ss=Automata(i-NoiseRadius:i+NoiseRadius,j-NoiseRadius:j+NoiseRadius);
            if (sum(sum(ss))>=1 && sum(sum(ss))<=NoiseThreshold)  %calculate neighbors sum
                AutomatonIndex(i,j)=-1;
                red=[red;j,Dim1Size-i];
                NoiseNum=NoiseNum+1;
                %                 p1=plot(j,Dim1Size-i,'o','MarkerEdgeColor','r',...
                %                     'MarkerFaceColor','r','MarkerSize',3);
            else
                green=[green;j,Dim1Size-i];
                NotNoiseData=[NotNoiseData;[i,j]];
                %                 p2=plot(j,Dim1Size-i,'o','MarkerEdgeColor','k',...
                %                     'MarkerFaceColor','g','MarkerSize',3);
            end
            
        end
    end
end

if size(red,1)>0
    p1=plot(red(:,1),red(:,2),'x','MarkerEdgeColor','r','MarkerFaceColor','b');
else
    p1=[];
end

if size(green,1)>0
    p2=plot(green(:,1),green(:,2),'o','MarkerEdgeColor','k','MarkerFaceColor','g','MarkerSize',3);
else
    p2=[];
end
xlabel('X');
ylabel('Y');

legStr = {'Noise','Data' };
legend([p1,p2] ,legStr);
t=title(['Noise Radius 1/2(L/S)= ',num2str(NoiseRadius),'    Num of Noises= ',num2str(NoiseNum), '    Noise Threshold= ',num2str(NoiseThreshold)],'Color','blue');

save('green.mat','green');
save('NotNoiseData','NotNoiseData');
save('DenoisedAutomata.mat','Automata');
save('DenoisedAutomatonIndex.mat','AutomatonIndex');

