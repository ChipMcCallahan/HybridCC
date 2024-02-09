from hybrid_cc.game.elements import instances
from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.game.elements.instances.bomb import Bomb
from hybrid_cc.game.elements.instances.button import Button
from hybrid_cc.game.elements.instances.chip import Chip
from hybrid_cc.game.elements.instances.cloner import Cloner
from hybrid_cc.game.elements.instances.corner import Corner
from hybrid_cc.game.elements.instances.dirt import Dirt
from hybrid_cc.game.elements.instances.dirt_block import DirtBlock
from hybrid_cc.game.elements.instances.door import Door
from hybrid_cc.game.elements.instances.exit import Exit
from hybrid_cc.game.elements.instances.fire import Fire
from hybrid_cc.game.elements.instances.fire_boots import FireBoots
from hybrid_cc.game.elements.instances.flippers import Flippers
from hybrid_cc.game.elements.instances.floor import Floor
from hybrid_cc.game.elements.instances.force import Force
from hybrid_cc.game.elements.instances.gravel import Gravel
from hybrid_cc.game.elements.instances.hint import Hint
from hybrid_cc.game.elements.instances.ice import Ice
from hybrid_cc.game.elements.instances.ice_block import IceBlock
from hybrid_cc.game.elements.instances.key import Key
from hybrid_cc.game.elements.instances.monster import Monster
from hybrid_cc.game.elements.instances.panel import Panel
from hybrid_cc.game.elements.instances.placeholder import Placeholder
from hybrid_cc.game.elements.instances.player import Player
from hybrid_cc.game.elements.instances.pop_up_wall import PopUpWall
from hybrid_cc.game.elements.instances.robot import Robot
from hybrid_cc.game.elements.instances.skates import Skates
from hybrid_cc.game.elements.instances.socket import Socket
from hybrid_cc.game.elements.instances.space import Space
from hybrid_cc.game.elements.instances.stepping_stone import SteppingStone
from hybrid_cc.game.elements.instances.suction_boots import SuctionBoots
from hybrid_cc.game.elements.instances.tank import Tank
from hybrid_cc.game.elements.instances.teleport import Teleport
from hybrid_cc.game.elements.instances.thief import Thief
from hybrid_cc.game.elements.instances.toggle_wall import ToggleWall
from hybrid_cc.game.elements.instances.trap import Trap
from hybrid_cc.game.elements.instances.trick_wall import TrickWall
from hybrid_cc.game.elements.instances.wall import Wall
from hybrid_cc.game.elements.instances.water import Water
from hybrid_cc.shared import Id, Direction
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.kwargs import DIRECTION, SIDES, COLOR, RULE, COUNT, \
    CHANNEL
from hybrid_cc.shared.tag import OVERRIDDEN, SLIDING

DEFAULT_KWARGS = {
    COLOR: Color.GREY,
    RULE: None,
    COUNT: 1,
    CHANNEL: 0,
    SIDES: "",
    DIRECTION: Direction.S
}


class ElemHandler:
    def __init__(self, level):
        self.id_to_class = {
            Id.BOMB: Bomb,
            Id.BUTTON: Button,
            Id.CHIP: Chip,
            Id.CLONER: Cloner,
            Id.CORNER: Corner,
            Id.DIRT: Dirt,
            Id.DIRT_BLOCK: DirtBlock,
            Id.DOOR: Door,
            Id.EXIT: Exit,
            Id.FIRE: Fire,
            Id.FIRE_BOOTS: FireBoots,
            Id.FLIPPERS: Flippers,
            Id.FLOOR: Floor,
            Id.FORCE: Force,
            Id.GRAVEL: Gravel,
            Id.HINT: Hint,
            Id.ICE: Ice,
            Id.ICE_BLOCK: IceBlock,
            Id.KEY: Key,
            Id.MONSTER: Monster,
            Id.PANEL: Panel,
            Id.PLACEHOLDER: Placeholder,
            Id.PLAYER: Player,
            Id.POP_UP_WALL: PopUpWall,
            Id.ROBOT: Robot,
            Id.SKATES: Skates,
            Id.SOCKET: Socket,
            Id.SPACE: Space,
            Id.STEPPING_STONE: SteppingStone,
            Id.SUCTION_BOOTS: SuctionBoots,
            Id.TANK: Tank,
            Id.TELEPORT: Teleport,
            Id.THIEF: Thief,
            Id.TOGGLE_WALL: ToggleWall,
            Id.TRAP: Trap,
            Id.TRICK_WALL: TrickWall,
            Id.WALL: Wall,
            Id.WATER: Water,
        }

        Elem.init_at_level_load()
        Mob.init_at_level_load()
        for attribute_name in dir(instances):
            element_class = getattr(instances, attribute_name)

            # Check if it's a class but not this class.
            if element_class is not self and isinstance(element_class, type):
                if hasattr(element_class, "init_at_level_load"):
                    init_elem_cls = getattr(element_class, "init_at_level_load")
                    init_elem_cls()

        # Element specific initializations.
        Socket.set_chips_required(level.chips.copy())

    def construct_at(self, p, _id, **kwargs):
        kwargs = self.assign_kwarg_defaults(**kwargs)
        instance_class = self.get_class(_id)
        constructor = getattr(instance_class, "construct_at")
        return constructor(p, **kwargs)

    @staticmethod
    def destruct_at(p, elem):
        instance_class = elem.__class__
        destructor = getattr(instance_class, "destruct_at")
        destructor(elem, p)

    def get_class(self, _id):
        if not self.id_to_class:
            raise TypeError(f"{self.__name__} was not initialized!")
        if _id not in self.id_to_class:
            raise TypeError(f"Id {_id} was not found in Elem class registry.")
        return self.id_to_class[_id]

    @staticmethod
    def assign_kwarg_defaults(**kwargs):
        new_kwargs = kwargs.copy()
        for kwarg in (COLOR, RULE, COUNT, CHANNEL, SIDES, DIRECTION):
            new_kwargs[kwarg] = kwargs.get(kwarg) or DEFAULT_KWARGS[kwarg]
        return new_kwargs

    def collect_move_plans(self, inputs, tick):
        moves, requests = [], []
        player_moves = []  # these happen second to last
        sliding_moves = []  # these happen last

        # Class level plans (e.g. ice, force floor, dpad buttons)
        for elem_class in self.id_to_class.values():
            method = getattr(elem_class, "do_class_planning", None)
            if method:
                new_moves, new_requests = method(inputs=inputs, tick=tick)
                for move in new_moves or []:
                    mob = Mob.instances[move.mob_id]
                    if mob.id == Id.PLAYER:    # This is the Player mob id
                        player_moves.append(move)
                    elif mob.tagged(SLIDING):
                        sliding_moves.append(move)
                    else:
                        moves.append(move)
                if new_requests:
                    requests.extend(new_requests)

        # Instance level plans (mobs)
        for mob_id, mob in Mob.instances.items():
            method = getattr(mob, "do_planning", None)
            if method:
                new_moves, new_requests = method(tick, inputs=inputs)

                # Don't do anything with the requests if overridden.
                if mob.tagged(OVERRIDDEN):
                    continue

                if new_moves:
                    # Player always moves last.
                    if mob.id == Id.PLAYER:
                        # Overriding force floors depends on this order
                        player_moves = new_moves + player_moves
                    else:
                        moves += new_moves
                if new_requests:
                    requests.extend(new_requests)

        return moves + player_moves + sliding_moves, requests

    @staticmethod
    def get_mob(mob_id):
        return Mob.get_mob(mob_id)
