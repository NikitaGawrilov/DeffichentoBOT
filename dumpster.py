@bot.command()
async def test(ctx):
    global test_is_running
    test_is_running = not test_is_running
    if test_is_running:
        DiscordComponents(bot)
        msg = await ctx.send(
            "Поймал?",
            components=[
                Button(label="Ага", custom_id="btnY"),
                Button(label="Неа", custom_id="btnN")
            ]
        )

        @bot.event
        async def on_button_click(interaction):
            if interaction.author.id == ctx.author.id:
                if interaction.custom_id == "btnY":
                    await interaction.respond(content="Чотк")
                    global test_is_running
                    test_is_running = False
                    await msg.edit(content="...", components=[])
                    return
                elif interaction.custom_id == "btnN":
                    await interaction.respond(content="Лох")
                    await msg.edit(content="...", components=[])
                    test_is_running = False
                    return
                else:
                    pass
            else:
                await interaction.respond(content="Это не тебе!")
    else:
        await ctx.send("Уже запущен")
        return

    # def check(interaction):
    #     return (interaction.custom_id == "btnY" or interaction.custom_id == "btnN") and interaction.author.id in players
    #
    # while True:
    #     interaction = await bot.wait_for("button_click", check=check)
    #     if interaction.author.id == ctx.author.id:
    #         if interaction.custom_id == "btnY":
    #             await interaction.respond(content="Чотк", type=1)
    #             interaction.responded = False
    #             return
    #         elif interaction.custom_id == "btnN":
    #             await interaction.respond(content="Лох")
    #             interaction.responded = False
    #             return
    #         else:
    #             pass
    #     else:
    #         await interaction.respond(content="Это не тебе!")
    #         interaction.responded = False