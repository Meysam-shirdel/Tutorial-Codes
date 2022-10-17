%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Data to Automata
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc
clear all
close all

% load X.mat
% Data=unique(X,'rows');
% % -----------------------
load SData.mat
Data=unique(X,'rows');
% % -----------------------
% load flame.mat
% Data=unique(Flame,'rows');
% % -----------------------
% load sizes2.mat
% Data=unique( sizes2,'rows');
% % -----------------------
% load triangle2.mat
% Data=unique( triangle2,'rows');
% % -----------------------
% load S1.mat;
% Data=unique(Data,'rows');
% % -----------------------


 figure(1)
 hold on
% plot(Data(:,1),Data(:,2),'o','Color',[0.4940 0.1840 0.5560],'MarkerFaceColor','b','MarkerSize',3);
% xlabel('X');
% ylabel('Y');
% t=title('Main Data','Color','blue');
% X = rand(3,2);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DataSize=size(Data,1);
% Z=pdist(Data);
% Distance= squareform(Z)
for i=1:DataSize
    for j=1:DataSize
        if i==j
            Distance(i,j)=inf;
        else
            Distance(i,j)=(sum((Data(i,1:2)-Data(j,1:2)).^2)).^0.5;
        end
    end
end

mins1=sort(min(Distance,[],2));
FieldExpansion=max(mins1(1:end-1,1));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Dim1Min=min(Data(:,1));
Dim1Max=max(Data(:,1));
Dim2Min=min(Data(:,2));
Dim2Max=max(Data(:,2));

axis([Dim1Min-FieldExpansion Dim1Max+FieldExpansion Dim2Min-FieldExpansion Dim2Max+FieldExpansion])
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
MinGridLength=min(min(Distance));
GridLength=MinGridLength-eps;
NoiseRadius=ceil((FieldExpansion/GridLength)/2);

Dim1UpperLimit=ceil(((Dim1Max+FieldExpansion)-(Dim1Min-FieldExpansion))/(GridLength));
Dim2UpperLimit=ceil(((Dim2Max+FieldExpansion)-(Dim2Min-FieldExpansion))/(GridLength));
Automata=zeros(Dim2UpperLimit,Dim1UpperLimit);
AutomatonIndex=Automata;
BD=Data;
for k=1:DataSize
    iCell(k)=ceil(abs(Data(k,1)-(Dim1Min-FieldExpansion))/(GridLength)); %%Distance from data point and start of dimension i of Automata/ gridlength
    jCell(k)=ceil(abs(Data(k,2)-(Dim2Min-FieldExpansion))/(GridLength));
    BD(k,4)=iCell(k);
    BD(k,5)=jCell(k);
    Automata(Dim2UpperLimit-jCell(k)+1,iCell(k)+1)=1;
    AutomatonIndex(Dim2UpperLimit-jCell(k)+1,iCell(k)+1)=2;
end

MandN=[iCell;jCell]';
MandN=unique(MandN,'rows');
MandNSize=size(MandN,1);

DataLoss=DataSize-MandNSize;
AutomatonIndex=AutomatonIndex-2*ones(Dim2UpperLimit,Dim1UpperLimit);

Dim1Size=size(Automata,1);
Dim2Size=size(Automata,2);
[XGrid,YGrid]=meshgrid(1:Dim2Size,1:Dim1Size);
% plot Automata
plot(XGrid,YGrid,'.','color',[0.9 0.9 0.9])
axis([1 Dim2Size 1 Dim1Size])
% plot live automatons
for i=1:Dim1Size
    for j=1:Dim2Size
        if Automata(i,j)==1
            plot(j,Dim1Size-i,'o','MarkerEdgeColor','k',...
                'MarkerFaceColor','b','MarkerSize',3)
        end
    end
end
hold off
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
save('NoiseRadius.mat','NoiseRadius')
save('Automata.mat','Automata')
save('AutomatonIndex.mat','AutomatonIndex')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%