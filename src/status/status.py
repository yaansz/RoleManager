from enum import Enum
import random

class Status(Enum):
    Watching = ['Aula do Braida boa d+ slk', '🍻', 'One Piece', 'Netflix', 'Disney+', 'HBO MAX', 'Cuphead',
    'meia noite eu te conto', 'As memórias de Marnie', 'A viagem de Chihiro', 'Luca', 'Raya e o Último Dragão',
    'Vidas ao Vento', 'O Conto da Princesa Kaguya', 'Looney Tunes', 'Irmão do Jorel', 'Hora de Aventura', 'Ponyo',
    'Susurros do Coração', 'Posso ouvir o oceano', 'O Serviço de Entregas da Kiki', 'Meu Amigo Totoro',
    'John Wick - De Volta ao Jogo', 'John Wick - Um Novo Dia para Matar', 'John Wick - Parabellum', 'John Wick bom d+',
    'Cruella', 'Pequena Sereia']
    Playing = ['Jogando', 'Playing', 'Talvez?', 'Boa Pergunta', '😳', '🍻', 'minha vida no lixo',
    'Cuphead', 'Undertale', 'guilty gear', 'no hard', 'segredo xiii', 'meia noite eu te conto',
    'vava?', 'r6zin', 'steam sale', 'Enter the Gungeon 🔫', 'Celeste 💖', 'Kandidatos', 'Brawlhalla',
    'Fall Guys', 'Amongus', 'PUBG?', 'Hollow Knight', 'PAYDAY 2', 'Apex Legends', 'UNO', 'Dead by Daylight']
    Listening = ['rei do gado', 'boa noite meu consagrado', 'bom dia meu chegado', 'mc poze nos anos 80', 'Skrillex',
    'Porter Robinson', 'Trilha sonora de space jam', 'Jonas Brothers', 'Joe Hisaishi', 'Tyler, The Creator', 'Tiao, o criador',
    'Kendrick Lamar', 'G-Eazy', 'OST de Undertale', 'OST de Chihiro', 'Gorillaz', 'Gorillaz - DARE', '911', 'EARFQUAKE', 
    'See You Again', 'Juggernaut', 'Shelter', 'Wind Tempos', 'Sweden', 'OST do Minecraft', 'Covet', 'Plastic Beach', 'Kero Kero Bonito',
    'Cut My Lip', 'Kali Uchis', 'KALI UCHIS', 'KaLi UcHis', 'telepatia', 'Yvette Young', 'Travis Scott', 'ASTROWORLD', 'Choice', 'Madeon', 
    'Nurture', 'Worlds']
    Streaming = ['Jogando', '😳', '🍻', 'meus fracassos', 'minhas vitórias', 'Rainbow6', 'cod 4',
    'Liga das Lendas', 'Cuphead', 'guilty gear', 'KKKJ', 'Kampeonato de Kandidatos', 'segredo xiii', 
    'meia noite eu te conto', 'arrasta pra cima que eu te conto', 'Streaming', 'Transmitindo',
    'será?', 'cringe 😡😔🤮', 'calma lá meu parceiro']
    Idle = ['Muito ocupado', 'Não pertube', 'Talvez?', 'Sim', 'Não', 'Boa Pergunta', '😳', '🍻', 
    'Fazendo: prova de arq2', 'triste', 'AAAAAAAAAAAAAAAAAA', 'dale', 'deveras intelectus', 'será?', 
    'cringe 😡😔🤮', 'calma lá meu parceiro', 'a morte do romantismo', 'passa o zap rs??', 'antisocial se afaste 😶',
    'minina veneno meu pinto é pequeno', 'ó o toro kkkkk ata são só minnhas lágrimas', 'amem', 'SHALOM', 'mo paz']

