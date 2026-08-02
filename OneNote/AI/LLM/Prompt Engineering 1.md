**提示词框架**  
一个提示词是由指令、上下文、输入数据和输出指示这几个要素中的一个或多个组成的，这其实就为如何编写提示词提供了一个基础框架，最初在 [《](https://www.promptingguide.ai/introduction/elements)Prompt Engineering Guide》 中总结的  
一种是CRISPE框架：  
CR： Capacity and Role（能力与角色）。你希望 ChatGPT 扮演怎样的角色。  
I： Insight（洞察力），背景信息和上下文。  
S： Statement（指令），你希望 ChatGPT 做什么。  
P： Personality（个性），你希望 ChatGPT 以什么风格或方式回答你。  
E： Experiment（实验），要求 ChatGPT 为你提供多个答案。  
一种结构化提示词  
`# Role: Your_Role_Name`  
   
`## Profile`  
   

```
- Author: YZFly
- Version: 0.1
- Language: English or 
```

中文

```
 or Other language
- Description: Describe your role. Give an overview of the character's characteristics and skills
```
    

```
### Skill 1
1. xxx
2. xxx
```
    

```
### Skill 2
1. xxx
2. xxx
```
    

```
## Rules
1. Don't break character under any circumstance.
2. Don't talk nonsense and make up facts.
```
    

```
## Workflow
1. First, xxx
2. Then, xxx
3. Finally, xxx
```
    

```
## Initialization
As a/an \<Role\>, you must follow the \<Rules\>, you must talk to user in default \<Language\>
```

，

```
you must greet the user. 
Then introduce yourself and introduce the \<Workflow\>
```

.  
零样本提示（Zero-shot Prompting） vs. 少样本提示（Few-shot Prompting）