clear all
close all
clc
%%
periodos=40;
ops=6;
time_op=[2*60,10*60];
mean_op=[100,1000];
amp_op=[50,100];
time_stop=[1*60,5*60];
updown=[10,30];
dt=1;

formas=[1:1:7]; % 0 plana, 1 ascendente, 2 descendente, 3 harmonico, 4 step up, 5 step down, 6 rampa down, 7 rampa down

op.form=randi([min(formas),max(formas)],ops,1);
op.dur=randi(time_op,ops,1);
op.mean=randi(mean_op,ops,1);
op.amp=randi(amp_op,ops,1);
op.stop=randi(time_stop,ops,1);
op.updown=randi(updown,ops,1);
% op.stop(1)=op.stop(1)+10*60;
pot_noise=randi([5,10],1);

tabla=zeros(ops*periodos,2);
[per_m,op_m]=meshgrid([1:1:periodos],[1:1:ops]);

tabla(:,1)=per_m(:);
tabla(:,2)=op_m(:);

%%
tic
for cont=1:length(tabla)    
    % parte de señal=0
    time_stop=[dt:dt:op.stop(tabla(cont,2))*randi([5,15],1)/10];    
    serie_stop= pot_noise*rand(size(time_stop)).*randi([-1,1],size(time_stop));
    
    % introducción de errores aleatorios
    % variación de duración
    t_mod=1;
    if rand>0.98 % 2% de OPs con variación
        t_mod=randi([95,105],1)/100; % variación entre 95 y 105 %
    end
    time_op=[dt:dt:op.dur(tabla(cont,2))*t_mod];
    
    % variación de valor medio
    mean_mod=1;
    if rand>0.9 % 10% de OPs con variación
        mean_mod=randi([95,105],1)/100; % variación entre 95 y 105 %
    end
    mean_op=op.mean(tabla(cont,2))*mean_mod;

    % variación de amplitud
    amp_mod=1;
    if rand>0.95 % 5% de OPs con variación
        amp_mod=randi([80,120],1)/100; % variación entre 80 y 120 %
    end
    amp_op=op.amp(tabla(cont,2))*amp_mod;
    
    % variación de amplitud de ruido
    mod_noise=1;
    if rand>0.95 % 5% de OPs con variación
        mod_noise=randi([110,150],1)/100; % variación entre 110 y 150 %
    end

    % variación de forma
    form_op=op.form(tabla(cont,2));
%     if rand>0.98 % 2% de OPs con variación
%         form_op=randi([min(formas),max(formas)],1,1);
%     end

    % calculo de valores para las series en función de su forma
    switch form_op
        case 0
            serie_op=mean_op*ones(size(time_op))+pot_noise*mod_noise*rand(size(time_op)).*randi([-1,1],size(time_op));
        case 1            
            serie_op=linspace(mean_op,mean_op+amp_op,(length(time_op)))+pot_noise*mod_noise*rand(size(time_op)).*randi([-1,1],size(time_op));
        case 2
            serie_op=linspace(mean_op,mean_op-amp_op,(length(time_op)))+pot_noise*mod_noise*rand(size(time_op)).*randi([-1,1],size(time_op));
        case 3
            serie_op=mean_op+amp_op*cos(time_op/max(time_op)*5)+pot_noise*mod_noise*rand(size(time_op)).*randi([-1,1],size(time_op));
        case 4
            serie_op=[mean_op*ones(1,ceil(length(time_op)/2)),(mean_op+2*amp_op)*ones(1,floor(length(time_op)/2))]+pot_noise*mod_noise*rand(size(time_op)).*randi([-1,1],size(time_op)); %+10*rand(size(time_op)).*randi([-1,1],size(time_op));
        case 5
            serie_op=[mean_op*ones(1,ceil(length(time_op)/2)),(mean_op-2*amp_op)*ones(1,floor(length(time_op)/2))]+pot_noise*mod_noise*rand(size(time_op)).*randi([-1,1],size(time_op)); %+10*rand(size(time_op)).*randi([-1,1],size(time_op));
        case 6
            tp=[floor(length(time_op)/3),floor(2*length(time_op)/3),length(time_op)];
            serie_op=[mean_op*linspace(1,1,tp(1)),linspace(mean_op,mean_op-2*amp_op,tp(2)-tp(1)),(mean_op-2*amp_op)*linspace(1,1,(tp(3))-tp(2))]+pot_noise*mod_noise*rand(size(time_op)).*randi([-1,1],size(time_op));
        case 7
            tp=[floor(length(time_op)/3),floor(2*length(time_op)/3),length(time_op)];
            serie_op=[mean_op*linspace(1,1,tp(1)),linspace(mean_op,mean_op+2*amp_op,tp(2)-tp(1)),(mean_op+2*amp_op)*linspace(1,1,(tp(3))-tp(2))]+pot_noise*mod_noise*rand(size(time_op)).*randi([-1,1],size(time_op));
    end

    % rampas de inicio/final
    serie_op(1:op.updown(tabla(cont,2))/dt)=serie_op(1:op.updown(tabla(cont,2))/dt)-linspace(serie_op(1),0,op.updown(tabla(cont,2))/dt);
    serie_op(length(time_op)-op.updown(tabla(cont,2))/dt+1:length(time_op))=serie_op(length(time_op)-op.updown(tabla(cont,2))/dt+1:length(time_op))-linspace(0,serie_op(length(time_op)),op.updown(tabla(cont,2))/dt);
    
    % guardado de vectores de tiempo, serie e identificadores de periodo y OP
    if cont==1
        time_op=time_op+time_stop(end);
        time=[time_stop,time_op];
        serie=[serie_stop,serie_op];
        f_periodo=tabla(cont,1)*ones(size([serie_stop,time_op]));
        f_op=[zeros(size(serie_stop)),tabla(cont,2)*ones(size(time_op))];
    else
        time_stop=time_stop+time(end);
        time_op=time_op+time_stop(end);
        time=[time,time_stop,time_op];
        serie=[serie,serie_stop,serie_op];
        f_periodo=[f_periodo,tabla(cont,1)*ones(size([serie_stop,time_op]))];
        f_op=[f_op,[zeros(size(serie_stop)),tabla(cont,2)*ones(size(time_op))]];
    end
end
t_serie=toc
%%
% tic
% figure
% plot(time,serie)
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
tic
for cont_op=1:ops
    colores=jet(periodos);
    figure
    for cont=1:periodos
        id1=find(f_periodo==cont);
        id2=find(f_op==cont_op);
        id=intersect(id1,id2);
        plot(time(id)-min(time(id)),serie(id),'color',colores(cont,:))
        hold on
    end
    title(['Op - ' num2str(cont_op)])
    xlabel('Time - s')    
end
t_plot_ops=toc

