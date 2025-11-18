
# 🐾 PetVida — Sistema de Gestão de Clínica Veterinária  

## 🧩 Visão Geral  
O **PetVida** é um sistema  de gestão de serviços para clínicas veterinárias e PetShops, desenvolvido em **Django (backend)** e integrado com um **aplicativo Flutter (frontend mobile)**.  

O sistema permite:  
- Cadastrar clientes e seus animais.  
- Gerenciar agendamentos de serviços.  
- Finalizar atendimentos e notificar automaticamente o cliente via **Firebase Cloud Messaging (FCM)**.  
- Controlar os horários de agendamento, exibindo apenas horários válidos.  
- Atualizar automaticamente as telas tanto no painel web (Django) quanto no app Flutter.  

---

## ⚙️ Tecnologias Utilizadas  

### Backend (Django)
- **Django 5.x** + **Django REST Framework**  
- **MySQL** como banco de dados principal  
- **Bootstrap 5** no painel administrativo  
- **Firebase Admin SDK** para envio de notificações  
- **Django Auth** com integração automática de usuários  

### Frontend Mobile (Flutter)
- **Flutter 3.x**  
- **Firebase Messaging (FCM)**  
- **Dio** para comunicação com a API Django  
- **Atualização automática de telas** após login, novos agendamentos e finalizações de serviços  
- **Tema visual padronizado (verde PetVida)**  

---

## 👤 Cadastro de Clientes Automatizado  
Durante o cadastro de um novo cliente no painel Django:
- Um **usuário Django** é criado automaticamente com o mesmo nome e e-mail.  
- A senha padrão é o **telefone informado no cadastro** (mesmo sendo considerada fraca).  
- O campo `fcm_token` é mantido no modelo, permitindo o envio de notificações diretamente para o app Flutter.  

---

## 🐶 Cadastro de Animais  
O formulário de cadastro de animais foi aprimorado com:
- Dropdowns para **Espécie** (`Cachorro`, `Gato`) e **Porte** (`Pequeno`, `Médio`, `Grande`);  
- Exibição automática do tutor vinculado (cliente responsável).  

---

## 🕓 Agendamentos de Serviços  
### Lado Django:
- Exibe os agendamentos do dia com atualização automática a cada 60 segundos.  
- Botão de **“Finalizar Serviço”** muda o status visual do card e bloqueia novos cliques.  
- Ao finalizar um serviço, o cliente recebe **uma notificação FCM**.  

### Lado Flutter:
- Tela de **“Meus Agendamentos”** com atualização automática.  
- Quando o cliente clica na notificação, o app é aberto e o card referente ao agendamento aparece com **cor cinza**, ícone de **check** e texto **“Serviço finalizado”**.  

---

## 🚀 Lógica de Agendamento Inteligente  
A API e a view de agendamento foram ajustadas para:
- Exibir apenas **horários futuros** no mesmo dia;  
- Remover automaticamente horários anteriores à hora atual;  
- Bloquear sobreposição de horários com base na duração dos serviços;  
- Permitir fácil extensão de horários (por exemplo, funcionamento até 20h).  

---

## 🔔 Notificações Firebase (FCM)  
- O servidor Django envia notificações push via **Firebase Cloud Messaging**.  
- O app Flutter exibe as notificações, mesmo com o app em segundo plano.  
- Ao clicar na notificação, o usuário é redirecionado diretamente para a tela de agendamentos atualizada.  

---

## 💻 Interface Django  
Principais telas implementadas:
- **Menu principal**  
- **Cadastro de clientes, animais e serviços**  
- **Agendamentos do dia (auto-refresh)**  
- **Agendar serviço rápido** (com horários livres e ocupados)   

## 📲 Integração com o App Flutter
- Login com autenticação Django REST + Token.  
- Registro automático do **token FCM** no servidor após o login.  
- Recebimento e exibição das notificações push.  
- Atualização automática da tela após novos agendamentos ou finalizações.  


## 🧪 Funcionalidades Testadas
✅ Login e autenticação via API  
✅ Cadastro automático de usuário Django ao criar cliente  
✅ Envio e recepção de notificações FCM  
✅ Atualização em tempo real de cards e listas  
✅ Filtragem de horários inválidos no agendamento  
✅ Auto-refresh na tela de agendamentos do dia  


## 📘 Autor
**Carlos Heiden**  
Desenvolvimento full stack (Django + Flutter) — Projeto acadêmico e funcional para clínicas veterinárias.  
