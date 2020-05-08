import discord
import pytest

from inhouse_bot.common_utils import discord_token
from inhouse_bot.sqlite.player_rating import PlayerRating
from inhouse_bot.sqlite.sqlite_utils import get_session
from inhouse_bot.sqlite.player import Player

session = get_session()
client = discord.Client()


@pytest.mark.asyncio
async def test_player():
    """
    Tests the addition of the Bot user as a player itself.
    Also tests PlayerRating and makes sure the on_cascade flags are applied properly.
    """
    await client.login(discord_token)

    test_user = await client.fetch_user(707853630681907253)

    player = Player(test_user)

    player = session.merge(player)
    session.commit()

    assert player == session.query(Player).filter(Player.discord_id == test_user.id).one()

    player_rating = PlayerRating(player, 'mid')

    session.add(player_rating)
    session.commit()

    assert player.ratings

    session.delete(player)
    session.commit()

    assert session.query(Player).filter(Player.discord_id == test_user.id).one_or_none() is None
    assert session.query(PlayerRating).filter(PlayerRating.player_id == test_user.id).one_or_none() is None
