{-# LANGUAGE OverloadedStrings #-}
import Data.Text qualified as T
import Data.Text.IO qualified as IO
import Data.Sequence (Seq(..), fromList, update, index)
import Data.Bits ((.&.), (.|.))

type Register = Seq Int
type Opcode = Int
type InsOut = (Int, Int, Int)
type Instruction = (Opcode, InsOut)
type Operation = InsOut -> Register -> Register
type Example = (Register, Instruction, Register)

addr :: Operation
addr (a, b, c) r = update c (index r a + index r b) r
addi (a, b, c) r = update c (index r a + b) r
mulr (a, b, c) r = update c (index r a * index r b) r
muli (a, b, c) r = update c (index r a * b) r
banr (a, b, c) r = update c (index r a .&. index r b) r
bani (a, b, c) r = update c (index r a .&. b) r
borr (a, b, c) r = update c (index r a .|. index r b) r
bori (a, b, c) r = update c (index r a .|. b) r
setr (a, b, c) r = update c (index r a) r
seti (a, b, c) = update c a
gtir (a, b, c) r = update c (if a > index r b then 1 else 0) r
gtri (a, b, c) r = update c (if index r a > b then 1 else 0) r
gtrr (a, b, c) r = update c (if index r a > index r b then 1 else 0) r
eqir (a, b, c) r = update c (if a == index r b then 1 else 0) r
eqri (a, b, c) r = update c (if index r a == b then 1 else 0) r
eqrr (a, b, c) r = update c (if index r a == index r b then 1 else 0) r

functions :: [Operation]
functions = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

parseExample :: T.Text -> Example
parseExample t = (beforeRegister, (opcode, (a, b, c)), afterRegister)
    where (before:middle:after:_) = T.splitOn "\n" t
          parseRegister = fromList . read . T.unpack . last . T.splitOn ": "
          beforeRegister = parseRegister before
          afterRegister = parseRegister after
          (opcode:a:b:c:_) = map (read . T.unpack ) (T.splitOn " " middle)

parseInput :: T.Text -> ([Example], a)
parseInput text = (map parseExample (T.splitOn "\n\n" firstPart), undefined)
    where (firstPart:secondPart:_) = T.splitOn "\n\n\n" text

howManyFitExample :: Example -> Int
howManyFitExample (input, (_, io), output) = sum $ map (fromEnum . (\fun -> fun io input == output)) functions

main :: IO ()
main = do
    (examples, _) <- parseInput <$> IO.readFile "input.txt"
    print examples
    print $ sum $ map (fromEnum . (>=3) . howManyFitExample) examples
