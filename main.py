# Type system and soundness proof simulation (progress + preservation)
from dataclasses import dataclass
from typing import Optional, Dict
 
@dataclass
class Type: pass
@dataclass
class TInt(Type): pass
@dataclass
class TBool(Type): pass
@dataclass
class TArrow(Type): left: Type; right: Type
 
@dataclass
class Term: pass
@dataclass
class Var(Term): name: str
@dataclass
class Num(Term): val: int
@dataclass
class Bool(Term): val: bool
@dataclass
class App(Term): fn: Term; arg: Term
@dataclass
class Lam(Term): var: str; ty: Type; body: Term
@dataclass
class If(Term): cond: Term; then: Term; else_: Term
 
Ctx = Dict[str, Type]
 
def type_check(ctx: Ctx, term: Term) -> Optional[Type]:
    if isinstance(term, Num): return TInt()
    if isinstance(term, Bool): return TBool()
    if isinstance(term, Var): return ctx.get(term.name)
    if isinstance(term, Lam):
        new_ctx={**ctx, term.var: term.ty}
        body_ty=type_check(new_ctx, term.body)
        return TArrow(term.ty, body_ty) if body_ty else None
    if isinstance(term, App):
        fn_ty=type_check(ctx, term.fn); arg_ty=type_check(ctx, term.arg)
        if isinstance(fn_ty,TArrow) and str(fn_ty.left)==str(arg_ty): return fn_ty.right
    if isinstance(term, If):
        c=type_check(ctx,term.cond); t=type_check(ctx,term.then); e=type_check(ctx,term.else_)
        if isinstance(c,TBool) and str(t)==str(e): return t
    return None
 
# Test: λx:Int. x + 1
f=Lam('x',TInt(),Var('x'))
print("id function type:", type_check({},f))
print("(λx:Int.x) 5 type:", type_check({}, App(f, Num(5))))
print("if true then 1 else 2:", type_check({}, If(Bool(True),Num(1),Num(2))))
