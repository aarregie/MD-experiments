clear all
close all
clc
%%

cd D:\repositorios-local\motif-discovery\

periodos=8; %Número de ejecuciones de cada proceso
ops=4; %Número de fases en cada proceso
time_op=[2*60,10*60];
mean_op=[0,10];
amp_op=[0,1];
time_stop=[0.5*60,2*60];
dt= 1; %Frecuencia de sampleo

formas=[0:1:3]; % 0 plana, 1 ascendente, 2 descendente, 3 harmonico

op.form=randi([min(formas),max(formas)],ops,1); %Secuencia de formas que tendrá todo el proceso
op.dur=randi(time_op,ops,1); %Duración de cada "forma" a lo largo del proceso
op.mean=randi(mean_op,ops,1); %Valor medio de cada forma a lo largo del proceso
op.amp= 0.1*rand(ops, 1); %Amplitud de cada forma a lo largo del proceso randi(amp_op,ops,1)
op.stop=zeros(ops,1); %Tiempo en zona de "no trabajo" (en torno al 0) %randi(time_stop,ops,1)
op.stop(1)=op.stop(1)+10*150; %Se aumenta el primer tramo de "no trabajo" en 600 puntos


tabla=zeros(ops*periodos,2);
[per_m,op_m]=meshgrid([1:1:periodos],[1:1:ops]);

tabla(:,1)=per_m(:);
tabla(:,2)=op_m(:);

%%
tic
for cont=1:length(tabla)    


    if rand>0.9
        t_mod=randi([9,11],1)/10;
    else
        t_mod=1;
    end
        time_op=[dt:dt:op.dur(tabla(cont,2))*t_mod];
    switch op.form(tabla(cont,2))
        case 0
            serie_op=op.mean(tabla(cont,2))*ones(size(time_op))+0.2*rand(size(time_op)); %randi([-1,1],size(time_op))
        case 1            
            serie_op=linspace(op.mean(tabla(cont,2)),op.mean(tabla(cont,2))+op.amp(tabla(cont,2)),(length(time_op)))+0.2*rand(size(time_op));
        case 2
            serie_op=linspace(op.mean(tabla(cont,2)),op.mean(tabla(cont,2))-op.amp(tabla(cont,2)),(length(time_op)))+0.2*rand(size(time_op));
        case 3
            serie_op=op.mean(tabla(cont,2))+op.amp(tabla(cont,2))*cos(time_op/max(time_op)*5)+0.5*rand(size(time_op));
    end

    if op.stop(tabla(cont,2)) ~= 0
        time_stop=[dt:dt:op.stop(tabla(cont,2))*randi([5,15],1)/10];
        serie_stop=0.3*rand(size(time_stop));
    else
        time_stop = [time_op(end)+1];
        serie_stop = [serie_op(end)+0.2*rand(1)];
        %.*randi([-1,1],size(time_stop))
    end


    if cont==1
        time_op=time_op+time_stop(end);
        time=[time_stop,time_op];
        serie=[serie_stop,serie_op];
        f_periodo=tabla(cont,1)*ones(size(time_op));
        f_op=[zeros(size(time_stop)),tabla(cont,2)*ones(size(time_op))];
    else
        time_stop=time_stop+time(end);
        time_op=time_op+time_stop(end);
        time=[time,time_stop,time_op];
        serie=[serie,serie_stop,serie_op];
        f_periodo=[f_periodo,tabla(cont,1)*ones(size([time_stop,time_op]))];
        f_op=[f_op,[zeros(size(time_stop)),tabla(cont,2)*ones(size(time_op))]];
        
    end

    if cont == length(tabla)
        time_stop=[dt:dt:op.stop(1)*randi([5,15],1)/10];
        serie_stop=0.3*rand(size(time_stop));
        time=[time,time_stop];
        serie=[serie,serie_stop];
        f_periodo=[f_periodo,tabla(cont,1)*ones([1,2])];
        f_op=[f_op,[zeros(size(time_stop)),tabla(cont,2)*ones(size(time_op))]];
    end
end
t_serie=toc
serie = serie(:);
%%
% tic
figure
plot(time,serie)
% 
% figure
% for cont=1:periodos
%     id=find(f_periodo==cont);
%     plot(time(id),serie(id))
%     hold on
% end
% t_plot1=toc
% tic
% colores=jet(ops);
% for cont=1:ops
%     id=find(f_op==cont);
%     plot(time(id),serie(id),'.','color',colores(cont,:))
%     hold on
% end
% t_plot2=toc
%%
% op_fig=10;
% colores=jet(periodos);
% figure
% for cont=1:periodos
%     id1=find(f_periodo==cont);
%     id2=find(f_op==op_fig);
%     id=intersect(id1,id2);
%     plot(time(id)-time(id(1)),serie(id),'color',colores(cont,:))
%     hold on
% end
%    



%%

%STORE TABLE


series_table = table(serie);
series_table = renamevars(series_table, 'serie', 'var');
writetable(series_table,'data\data-gen-test.csv')


