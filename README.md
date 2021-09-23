# RoleManager

RoleManager is a complete bot to help your manage of your server. You can add new roles, link roles to a category or channel, and allow your members to get and remove roles.


## Background

[TODO]: <> (TODO: Verify that shit :D)

Role Manager was created with the goal of helping me and my friends on my personal server. We needed to create new roles to handle with every new college class or event that part of us would attend. We didn't want to ping everyone or ping one by one, so I started to create it. It's very relaxing to me, and a I want to evolve it while I still have time and desire to do i t.

# Getting Started

If you want to use the bot, just [invite](https://discord.com/oauth2/authorize?client_id=864559239187529749&scope=bot&permissions=8) him to your server, all commands will default to '.'. Just type '.help' and you'll see everything he can do.

## Basic commands

### Everyone

- *.get*  <**nothing** | **role name** > -> gets the role associated to the current channel or the specified role
- *.remove* <**nothing** | **role name** > -> removes the role associated to the current channel or the specified role
- *.rolelist* -> List every role that the bot can give to you

[TODO]: <> (TODO: Maybe a little gif of this in discord :D)

### Administrators

- *.create* <**none** | **category** | **channel** | **role name**> -> creates a new role based in the current channel or in the specified name
- *.delete* <**category** | **channel** | **role name**> -> deletes a existent role based in the current channel or in the specified name

## Others good features

### Archives / Trash
I implemented a system to have an *archives*, *trash* or something like that, basically, I want to keep a channel but I don't wanna have the role associated, so I just move it to a selected category.

Why it's useful? Situations like when the semester is over and you don't wanna use the chat of 'Data Structures' anymore, but the chat can be useful to other people in the future.

#### Commands

- *.archives* -> Set the archives in the current category

## Reaction Roles

Users can assign and unassign to themselves by reacting to a message with an emoji. The method to create it is very simple

### Commands

- *.init emoji-role* -> Starts to listen that message as a reaction emoji message
- *.addr* <**:emoji:**> <**:role:**> -> Add a reaction/role to the initialized message when replying to it
- *.remr* <**:emoji:** | **:role:**> -> Remove a reaction/role to the initialized message when replying to it
