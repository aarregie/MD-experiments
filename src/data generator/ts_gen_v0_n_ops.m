clear all
close all
clc
%%

cd D:\repositorios-local\motif-discovery\

%OP1
periodos1=15; %Número de ejecuciones de cada proceso
ops1=4; %Número de fases en cada proceso
time_op1=[2*60,10*60];
mean_op1=[0,10];
amp_op1=[0,1];
time_stop1=[0.5*60,2*60];
dt= 1; %Frecuencia de sampleo

formas1=[0:1:3]; % 0 plana, 1 ascendente, 2 descendente, 3 harmonico

op1.form=randi([min(formas1),max(formas1)],ops1,1); %Secuencia de formas que tendrá todo el proceso
op1.dur=randi(time_op1,ops1,1); %Duración de cada "forma" a lo largo del proceso
op1.mean=randi(mean_op1,ops1,1); %Valor medio de cada forma a lo largo del proceso
op1.amp= rand(ops1, 1); %Amplitud de cada forma a lo largo del proceso randi(amp_op,ops,1)
op1.stop=zeros(ops1,1); %Tiempo en zona de "no trabajo" (en torno al 0) %randi(time_stop,ops,1)
op1.stop(1)=op1.stop(1)+10*150; %Se aumenta el primer tramo de "no trabajo" en 600 puntos


%OP2
periodos2=6; %Número de ejecuciones de cada proceso
ops2=2; %Número de fases en cada proceso
time_op2=[5*60,10*60];
mean_op2=[0,5];
amp_op2=[0,1];
time_stop2=[0.5*60,2*60];

formas2=[1:1:2]; % 0 plana, 1 ascendente, 2 descendente, 3 harmonico

op2.form=randi([min(formas2),max(formas2)],ops2,1); %Secuencia de formas que tendrá todo el proceso
op2.dur=randi(time_op2,ops2,1); %Duración de cada "forma" a lo largo del proceso
op2.mean=randi(mean_op2,ops2,1); %Valor medio de cada forma a lo largo del proceso
op2.amp= rand(ops2, 1); %Amplitud de cada forma a lo largo del proceso randi(amp_op,ops,1)
op2.stop=zeros(ops2,1); %Tiempo en zona de "no trabajo" (en torno al 0) %randi(time_stop,ops,1)
op2.stop(1)=op2.stop(1)+10*150; %Se aumenta el primer tramo de "no trabajo" en 600 puntos

total_ops = ops1 + ops2;
total_periodos = periodos1 + periodos2;

tabla1=zeros(ops1*periodos1,2);
[per_m,op_m]=meshgrid([1:1:periodos1],[1:1:ops1]);

tabla1(:,1)=per_m(:);
tabla1(:,2)=op_m(:);
tabla1(:,3)=1;

tabla2=zeros(ops2*periodos2,2);
[per_m,op_m]=meshgrid([1:1:periodos2],[1:1:ops2]);

tabla2(:,1)=per_m(:);
tabla2(:,2)=op_m(:);
tabla2(:,3) = 2;

tabla = [tabla1; tabla2];

identificador = tabla(:, 2)*100 + tabla(:, 1);

indices_aleatorios = randperm(size(tabla, 1));

% Reordenar las filas de la matriz utilizando los índices aleatorios
tabla = tabla(indices_aleatorios, :);


%%
tic
for cont=1:length(tabla1)    
    if op1.stop(tabla1(cont,2)) ~= 0
        time_stop=[dt:dt:op1.stop(tabla1(cont,2))*randi([5,15],1)/10];
        serie_stop=rand(size(time_stop));
    else
        time_stop = [0];
        serie_stop = [0];
        %.*randi([-1,1],size(time_stop))
    end

    if rand>0.9
        t_mod=randi([9,11],1)/10;
    else

        t_mod=1;
    end
        time_op=[dt:dt:op1.dur(tabla1(cont,2))*t_mod];
    switch op1.form(tabla1(cont,2))
        case 0
            serie_op=op1.mean(tabla1(cont,2))*ones(size(time_op))+2*rand(size(time_op)); %randi([-1,1],size(time_op))
        case 1            
            serie_op=linspace(op1.mean(tabla1(cont,2)),op1.mean(tabla1(cont,2))+op1.amp(tabla1(cont,2)),(length(time_op)))+2*rand(size(time_op));
        case 2
            serie_op=linspace(op1.mean(tabla1(cont,2)),op1.mean(tabla1(cont,2))-op1.amp(tabla1(cont,2)),(length(time_op)))+2*rand(size(time_op));
        case 3
            serie_op=op1.mean(tabla1(cont,2))+op1.amp(tabla1(cont,2))*cos(time_op/max(time_op)*5)+10*rand(size(time_op));
    end 
    if cont==1
        time_op=time_op+time_stop(end);
        time=[time_stop,time_op];
        serie=[serie_stop,serie_op];
        f_periodo=tabla1(cont,1)*ones(size(time_op));
        f_op=[zeros(size(time_stop)),tabla1(cont,2)*ones(size(time_op))];
    else
        time_stop=time_stop+time(end);
        time_op=time_op+time_stop(end);
        time=[time,time_stop,time_op];
        serie=[serie,serie_stop,serie_op];
        f_periodo=[f_periodo,tabla1(cont,1)*ones(size([time_stop,time_op]))];
        f_op=[f_op,[zeros(size(time_stop)),tabla1(cont,2)*ones(size(time_op))]];
        
    end
end
t_serie=toc

%%
tic
for cont=1:length(tabla2)    

    if op2.stop(tabla2(cont,2)) ~= 0
        time_stop=[dt:dt:op2.stop(tabla2(cont,2))*randi([5,15],1)/10];
        serie_stop=rand(size(time_stop));
    else
        time_stop = [0];
        serie_stop = [0];
        %.*randi([-1,1],size(time_stop))
    end

    if rand>0.9
        t_mod=randi([9,11],1)/10;
    else
        t_mod=1;
    end
        time_op=[dt:dt:op2.dur(tabla2(cont,2))*t_mod];
    switch op2.form(tabla2(cont,2))
        case 0
            serie_op=op2.mean(tabla2(cont,2))*ones(size(time_op))+2*rand(size(time_op)); %randi([-1,1],size(time_op))
        case 1            
            serie_op=linspace(op2.mean(tabla2(cont,2)),op2.mean(tabla2(cont,2))+op2.amp(tabla2(cont,2)),(length(time_op)))+2*rand(size(time_op));
        case 2
            serie_op=linspace(op2.mean(tabla2(cont,2)),op2.mean(tabla2(cont,2))-op2.amp(tabla2(cont,2)),(length(time_op)))+2*rand(size(time_op));
        case 3
            serie_op=op2.mean(tabla2(cont,2))+op2.amp(tabla2(cont,2))*cos(time_op/max(time_op)*5)+10*rand(size(time_op));
    end 
    

    time_stop=time_stop+time(end);
    time_op=time_op+time_stop(end);
    time=[time,time_stop,time_op];
    serie=[serie,serie_stop,serie_op];
    f_periodo=[f_periodo,tabla2(cont,1)*ones(size([time_stop,time_op]))];
    f_op=[f_op,[zeros(size(time_stop)),tabla2(cont,2)*ones(size(time_op))]];
       

    if cont == length(tabla2)
        time_stop=[dt:dt:op2.stop(1)*randi([5,15],1)/10];
        serie_stop=rand(size(time_stop));
        time=[time,time_stop];
        serie=[serie,serie_stop];
        f_periodo=[f_periodo,tabla2(cont,1)*ones([1,2])];
        f_op=[f_op,[zeros(size(time_stop)),tabla2(cont,2)*ones(size(time_op))]];
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
writetable(series_table,'data\matlab-series-n-ops.csv')


