import unittest
import asyncio
from main import read_file, traverse_part2


class TestDay8(unittest.IsolatedAsyncioTestCase):
    async def test_ghost_traverse(self):
        nodes, sequence = read_file("2023/08/testdata/part2.txt")
        steps = await traverse_part2(nodes, sequence)
        self.assertEqual(steps, 6)


if __name__ == "__main__":
    asyncio.run(unittest.main())
