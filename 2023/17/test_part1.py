import unittest
import uuid
from main import read_file, part1, Block, Path, get_possible_directions, Direction


class TestDay17Part1(unittest.IsolatedAsyncioTestCase):
    def test_read_file(self):
        block = read_file("2023/17/testdata/1.txt")
        self.assertIsInstance(block, Block)
        self.assertEqual(block.grid[0][0].value, 2)
        self.assertEqual(block.grid[0][1].value, 4)

    def test_get_possible_directions(self):
        height = 13
        width = 13
        path1 = Path(uuid=uuid.uuid4(), value=0, travelled=[(0, 0)], directions=[])
        self.assertEqual(get_possible_directions(path1, height=height, width=width), [Direction.EAST, Direction.SOUTH])

        path2 = Path(uuid=uuid.uuid4(), value=0, travelled=[(0, 0), (1, 0)], directions=[Direction.EAST])
        self.assertEqual(get_possible_directions(path2, height=height, width=width), [Direction.EAST, Direction.SOUTH])

        path3 = Path(
            uuid=uuid.uuid4(),
            value=0,
            travelled=[(0, 0), (2, 0), (3, 0)],
            directions=[Direction.EAST, Direction.EAST, Direction.EAST],
        )
        self.assertEqual(get_possible_directions(path3, height=height, width=width), [Direction.SOUTH])

    async def test_part1(self):
        block = read_file("2023/17/testdata/1.txt")
        retval = await part1(block)
        self.assertEqual(retval, 102)


if __name__ == "__main__":
    unittest.main()
