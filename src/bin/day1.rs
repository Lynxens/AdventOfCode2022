fn main() {
    let input = parse(include_str!("../../data/day1/input.txt"));

    puzzle_1(&input);
    puzzle_2(&input);
}

fn parse(raw_input: &str) -> Vec<i32>
{
    let mut data: Vec<i32> = raw_input
        .split("\n\n")
        .map(
            |rucksack| rucksack
                .split("\n")
                .fold(0,  |sum: i32, calories| sum + calories.parse::<i32>().unwrap())
        )
        .collect();

    data.sort_by(|a, b| b.cmp(a));

    data
}

fn puzzle_1(rucksacks: &Vec<i32>) -> i32 {
    *rucksacks.first().expect("No solution found")
}

fn puzzle_2(rucksacks: &Vec<i32>) -> i32 {
    rucksacks.into_iter().take(3).sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_puzzle_1_example() {
        let input = parse(include_str!("../../data/day1/input_example.txt"));

        assert_eq!(puzzle_1(&input), 24000 as i32);
    }

    #[test]
    fn test_puzzle_1() {
        let input = parse(include_str!("../../data/day1/input.txt"));

        assert_eq!(puzzle_1(&input), 69501 as i32);
    }

    #[test]
    fn test_puzzle_2_example() {
        let input = parse(include_str!("../../data/day1/input_example.txt"));

        assert_eq!(puzzle_2(&input), 45000 as i32);
    }

    #[test]
    fn test_puzzle_2() {
        let input = parse(include_str!("../../data/day1/input.txt"));

        assert_eq!(puzzle_2(&input), 202346 as i32);
    }
}